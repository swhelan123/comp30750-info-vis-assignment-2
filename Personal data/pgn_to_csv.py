import csv
import re
from datetime import datetime, timezone


def parse_pgn(pgn_file):
    """Parse a PGN file and return a list of raw game dictionaries."""
    games = []
    current_headers = {}
    moves_lines = []
    in_moves = False

    with open(pgn_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                if in_moves and moves_lines:
                    moves_text = " ".join(moves_lines)
                    # Strip clock annotations like {[%clk 0:03:01.9]}
                    moves_text = re.sub(r"\{[^}]*\}", "", moves_text)
                    # Collapse extra whitespace
                    moves_text = re.sub(r"\s+", " ", moves_text).strip()
                    current_headers["Moves"] = moves_text
                    games.append(current_headers)
                    current_headers = {}
                    moves_lines = []
                    in_moves = False
                continue

            header_match = re.match(r'^\[(\w+)\s+"(.*)"\]$', line)
            if header_match:
                current_headers[header_match.group(1)] = header_match.group(2)
                in_moves = False
            else:
                in_moves = True
                moves_lines.append(line)

    # Handle last game if file doesn't end with a blank line
    if current_headers:
        if moves_lines:
            moves_text = " ".join(moves_lines)
            moves_text = re.sub(r"\{[^}]*\}", "", moves_text)
            moves_text = re.sub(r"\s+", " ", moves_text).strip()
            current_headers["Moves"] = moves_text
        games.append(current_headers)

    return games


def datetime_to_epoch_ms(date_str, time_str):
    """Convert 'YYYY.MM.DD' + 'HH:MM:SS' to epoch milliseconds (UTC)."""
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y.%m.%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    except (ValueError, TypeError):
        return ""


def extract_game_id(link):
    """Extract the numeric game ID from the Chess.com link."""
    if link:
        # e.g. https://www.chess.com/game/live/136891385990
        parts = link.rstrip("/").split("/")
        return parts[-1] if parts else ""
    return ""


def clean_moves(moves_text):
    """Remove move numbers and result token, leaving only SAN moves."""
    # Remove result at the end (1-0, 0-1, 1/2-1/2, *)
    moves_text = re.sub(r"\s*(1-0|0-1|1/2-1/2|\*)\s*$", "", moves_text)
    # Remove move numbers like "1." or "14..."
    moves_text = re.sub(r"\d+\.{1,3}\s*", "", moves_text)
    return moves_text.strip()


def count_turns(moves_text):
    """Count the number of half-moves (plies) in the cleaned move string."""
    if not moves_text:
        return 0
    return len(moves_text.split())


def determine_victory_status(termination):
    """Map Chess.com termination text to a victory_status category."""
    t = termination.lower()
    if "checkmate" in t or "mate" in t:
        return "mate"
    if "resign" in t:
        return "resign"
    if "time" in t and "drawn" not in t:
        return "outoftime"
    if "abandon" in t:
        return "resign"
    if "drawn" in t or "draw" in t:
        # Sub-categorise draws
        if "stalemate" in t:
            return "draw"
        if "insufficient" in t:
            return "draw"
        if "repetition" in t:
            return "draw"
        if "timeout" in t:
            return "draw"
        return "draw"
    return "resign"


def determine_winner(result, white, black, termination):
    """Return 'white', 'black', or 'draw'."""
    if result == "1-0":
        return "white"
    elif result == "0-1":
        return "black"
    else:
        return "draw"


def extract_opening_name(eco_url):
    """
    Derive a human-readable opening name from the ECOUrl.
    e.g. '.../openings/Italian-Game-Knight-Attack-Normal-Variation-5.exd5'
    becomes 'Italian Game: Knight Attack Normal Variation'
    """
    if not eco_url:
        return ""
    # Grab the last path segment
    slug = eco_url.rstrip("/").split("/")[-1]
    # Remove trailing move sequences like '-5.exd5' or '-2...dxe4-3.Nxe4-Nf6-4.Nxf6'
    # These start with a dash followed by a digit+dot pattern
    slug = re.sub(r"-\d+\..*$", "", slug)
    # Also remove trailing '-1...e5' style patterns
    slug = re.sub(r"-\d+\.\.\..+$", "", slug)
    # Replace hyphens with spaces
    name = slug.replace("-", " ")
    # Insert ': ' after the first main opening name segment if it looks like a variation
    # The ECOUrl typically has 'Opening-Name-Variation-Name'
    return name.strip()


def compute_opening_ply(eco_url, moves_text):
    """
    Estimate the opening ply from the ECOUrl.
    Count the number of move segments in the URL tail (e.g. '2...dxe4-3.Nxe4-Nf6-4.Nxf6' = 5 ply).
    If the URL has no move trail, estimate from the ECO code or default to a reasonable value.
    """
    if not eco_url:
        return ""
    slug = eco_url.rstrip("/").split("/")[-1]
    # Find trailing moves after the opening name
    # Pattern: a segment starting with a digit followed by a dot (e.g. '5.exd5')
    match = re.search(r"-(\d+\..*)$", slug)
    if match:
        move_trail = match.group(1)
        # Count individual SAN moves in the trail
        # Split on '-' and count tokens that look like moves
        tokens = re.split(r"-", move_trail)
        ply = 0
        for t in tokens:
            # Remove move number prefixes like '3.' or '2...'
            san = re.sub(r"^\d+\.{1,3}", "", t).strip()
            if san:
                ply += 1
        return ply
    # No moves in URL — estimate from the last move number in the slug
    # e.g. 'Indian-Game-2.c3' -> look for a pattern like '2.c3' somewhere
    match2 = re.search(r"-(\d+)\.([A-Za-z])", slug)
    if match2:
        # The move number * 2 - 1 gives approximate ply for a white move
        move_num = int(match2.group(1))
        return move_num * 2 - 1
    # Default: count moves in the cleaned moves list up to a small number
    # Just return empty if we can't determine
    return ""


def transform_game(raw):
    """Transform a raw PGN game dict into the target CSV schema."""
    # --- game_id ---
    game_id = extract_game_id(raw.get("Link", ""))

    # --- rated ---
    # Chess.com "Live Chess" games are rated by default; no explicit tag in PGN.
    # We can't know for certain, so we mark all as TRUE.
    rated = "TRUE"

    # --- start_time / end_time (epoch ms) ---
    start_time = datetime_to_epoch_ms(raw.get("UTCDate", ""), raw.get("StartTime", ""))
    end_time = datetime_to_epoch_ms(raw.get("EndDate", ""), raw.get("EndTime", ""))

    # --- moves (clean SAN only) ---
    raw_moves = raw.get("Moves", "")
    moves = clean_moves(raw_moves)

    # --- turns (number of half-moves / plies) ---
    turns = count_turns(moves)

    # --- victory_status ---
    termination = raw.get("Termination", "")
    victory_status = determine_victory_status(termination)

    # --- winner ---
    result = raw.get("Result", "")
    winner = determine_winner(result, raw.get("White", ""), raw.get("Black", ""), termination)

    # --- time_increment ---
    time_increment = raw.get("TimeControl", "").replace("/", "+")

    # --- players ---
    white_id = raw.get("White", "")
    white_rating = raw.get("WhiteElo", "")
    black_id = raw.get("Black", "")
    black_rating = raw.get("BlackElo", "")

    # --- opening ---
    opening_eco = raw.get("ECO", "")
    eco_url = raw.get("ECOUrl", "")
    opening_name = extract_opening_name(eco_url)
    opening_ply = compute_opening_ply(eco_url, moves)

    return {
        "game_id": game_id,
        "rated": rated,
        "start_time": start_time,
        "end_time": end_time,
        "turns": turns,
        "victory_status": victory_status,
        "winner": winner,
        "time_increment": time_increment,
        "white_id": white_id,
        "white_rating": white_rating,
        "black_id": black_id,
        "black_rating": black_rating,
        "moves": moves,
        "opening_eco": opening_eco,
        "opening_name": opening_name,
        "opening_ply": opening_ply,
    }


FIELDNAMES = [
    "game_id", "rated", "start_time", "end_time", "turns",
    "victory_status", "winner", "time_increment",
    "white_id", "white_rating", "black_id", "black_rating",
    "moves", "opening_eco", "opening_name", "opening_ply",
]


def pgn_to_csv(pgn_file, csv_file):
    """Convert a PGN file to a CSV matching the target schema."""
    raw_games = parse_pgn(pgn_file)

    if not raw_games:
        print("No games found in the PGN file.")
        return

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for raw in raw_games:
            row = transform_game(raw)
            writer.writerow(row)

    print(f"Successfully converted {len(raw_games)} games from '{pgn_file}' to '{csv_file}'.")


if __name__ == "__main__":
    pgn_path = "shanew012_games.pgn"
    csv_path = "shanew012_games.csv"
    pgn_to_csv(pgn_path, csv_path)

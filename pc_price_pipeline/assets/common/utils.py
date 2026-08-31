import hashlib
import pandas as pd

CPU_NAME_PATTERN = r"(?i)^(AMD Ryzen \d \w*|Intel Core Ultra \d+ \w*|Intel Core i\d+-\d+\w*|AMD Ryzen Threadripper ?(PRO)? \d*\w*|Intel Pentium \w*)"
CPU_BRAND_PATTERN = r"(?i)^(AMD|Intel)"
CPU_SOCKET_PATTERN = r"(?i)((?:AM\d)|(?:LGA \d+)|(?:sTR\w?\d)|(?:SP\w?\d)|(?:sWRX8))"
CPU_CORES_PATTERN = r"(?i)(\d+(?= ?-?(?:Cores|Core)))"
CPU_CLOCK_SPEED_PATTERN = r"(?i)(\d+\.?\d* ?(?:GHz|MHz))"
CPU_THREADS_PATTERN = r"(?i)(\d+(?= ?-?(?:Threads|Thread)))"
CPU_INTEGRATED_GRAPHICS_PATTERN = r"(?i)((?:Intel ?-?U?HD Graphics \d+|Iris|Radeon(?: HD \d+\w?| Vega \d+)?|Intel Xe))"
CPU_TDP_PATTERN = r"(?i)(\d+ ?W(?:att)?(?= ))"

GPU_BRAND_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+)?(\w+)"
GPU_MODEL_LINE_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+)?(?:\w+)(?<=)\s+(.*?)\s+(?=\b(?:Radeon|Geforce|Arc|AMD|NVIDIA)\b)"
GPU_CHIPSET_PATTERN_NVIDIA = r"(?:(?:GeForce\s?)(?:RTX|GTX|GT)?\s?(?:\d{2,4})(?:[\s-]+(?:Ti SUPER|Ti|SUPER|FE))?|RTX A\d{2,4})"
GPU_CHIPSET_PATTERN_AMD = r"(?:(?:Radeon\s?|AMD\s?)(?:RX\s|HD\s|AI Pro R)?(?:\d{2,4})(?:[\s-]+(?:XT|XTX|GRE))?|RX \d{2,4} (?:XT|XTX|GRE)?)"
GPU_CHIPSET_PATTERN_INTEL = r"(?:(?:Arc\s+)?(?:A|B)(?:\d+))"
GPU_CHIPSET_PATTERN = r"(?i)" + GPU_CHIPSET_PATTERN_NVIDIA + "|" + GPU_CHIPSET_PATTERN_AMD + "|" + GPU_CHIPSET_PATTERN_INTEL
GPU_MEMORY_PATTERN = r"(?i)((?!0)\d+\s?(?:GB|MB)|(?!0)\d+G)"
GPU_MEMORY_TYPE_PATTERN = r"(?i)(G?DDR\dX?)"
GPU_OVERCLOCKED_PATTERN = r"(?i)(?<!Non-)(?:Overclocked| OC|OC Edition|OC Edition|OC Version|Overclocked Edition|Overclocked Version)"

# TODO: MOBO SHOULD NOT BE USED ANYMORE
MOBO_BRAND_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+)?(\w+)"
MOBO_SOCKET_PATTERN = r"(?i)((?:AM\d)|(?:LGA\s?\d+)|(?:sTR\w?\d)|(?:SP\w?\d)|(?:sWRX8))"
MOBO_FORM_FACTOR_PATTERN = r"(?i)(Micro-ATX|mATX|Mini-ITX|ITX|ATX)"
MOBO_CHIPSET_PATTERN = r"(?i)([A-Z]\d{3}E?A?)"
MOBO_MEMORY_TYPE_PATTERN = r"(?i)(DDR\dX?)"

MOTHERBOARD_MODEL_LINE_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+|Memory module\s+)?(?:\w+)(?<=)\s+(.*?)\s+(?=\b(?:AM4|AM5|AMD|LGA ?\d+|Intel|Micro\s?-?ATX|mATX|Mini-ITX|ITX|ATX)\b)"
MOTHERBOARD_FORM_FACTOR_PATTERN = r"(?i)(Micro\s?-?ATX|mATX|Mini-ITX|ITX|ATX)"

MEMORY_BRAND_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+|Memory module\s+)?((?:G.SKILL)|\w+)"
MEMORY_MODEL_LINE_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+|Memory module\s+)?(?:\w+|G\.SKILL)(?<=)\s+(.*?)\s+(?=\b(?:\d{1,3}\w*?)\b)"
MEMORY_TYPE_PATTERN = r"(?i)(DDR\dX?)"
MEMORY_SPEED_PATTERN = r"(?i)(\b(?!DDR\d ?-?)(?:\d{4})\b|(?:\d{4}(?=MT/s))|(?:\d{4}(?=MHz)))"
MEMORY_CAPACITY_PATTERN = r"(?i)(?i)(\d+ ?GB)"
MEMORY_MODULES_PATTERN = r"(?i)(\d x \d+GB)"
MEMORY_CAS_LATENCY_PATTERN = r"(?i)(CL\d{2})"
MEMORY_COLOR_PATTERN = r"(?i)(?:\b(Black|White|Red|Blue|Green|Yellow|Silver|Gray|Grey|Orange|Purple)\b)"

STORAGE_BRAND_PATTERN = r"(?i)(?:Refurbished\s+|Open Box\s+)?(G.SKILL|Team Group|SK hynix|Western Digital|WD \w+(?: Plus| Pro)?|\w+)"
STORAGE_MODEL_LINE_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+|Memory module\s+)?(?:\w+(?: Group| Digital(?: \w+ WD)?| SSD| Power| hynix| electronics| memory| technology)?)(?<=)\s+(.*?)\s+(?=\b(?:\d+ ?(?:MB|GB|TB)|SSD|M\.2|NVMe|PCie|NAS|2\.5|SATA)\b)"
STORAGE_CAPACITY_PATTERN = r"(?i)(\d+ ?(?:GB|TB))"
STORAGE_FORM_FACTOR_PATTERN = r"(?i)(\d\.\d(?:\"|”)|\d\.\d ?-?(?:Inch|In)|M\.2(?:(?:-| )\d{2,4})?)"
STORAGE_INTERFACE_PATTERN = r"(?i)(PCI(?:e®?|-? ?Express(?: NVMe)?) (?:\d\.0|gen ?\d(?:\.0)?(?: NVMe)?)(?: ?X\d)?|m?SATA|SAS|Gen\d(?: NVMe| PCIe)|PCIe NVMe|SA510)"
STORAGE_TYPE_PATTERN = r"(?i)(SSD|HDD|Hard Disk Drive|Solid State Drive|Hard Drive)"

PSU_BRAND_PATTERN = r"(?i)(?:Refurbished\s+|Open Box\s+|Memory module\s+)?(Lian Li|Cooler Master|Super Flower|be quiet!?|Fractal Design|Dark Power|In ?-?win|\w+)"
PSU_MODEL_LINE_PATTERN = r"(?i)(?:Refurbished\s+|Open Box\s+|Memory module\s+)?(?:\w+(?: Flower| technology| Li| quiet!?| Master| Design| Power | ?-?win)?)(?<=)\s+(.*?)\s+(?=\b(?:ATX|SFX(?:-L)?|TFX|\d+ ?W(?:att)?|Cybenetics|80 ?Plus|80\+ |Fully|Platinum|PCIE ?\d|Series)\b)"
PSU_TYPE_PATTERN = r"(?i)(ATX|SFX(?:-L)?|TFX)"
PSU_EFFICIENCY_PATTERN = r"(?i)(80\s?(?:PLUS®?|\+)\s\w+|Cybenetics\s\w+|BRONZE|SILVER|GOLD|PLATINUM|TITANIUM)"
PSU_WATTAGE_PATTERN = r"(?i)(\d{3,}\s?W(?:att)?|RM\d+|CX\d+|SL-\d+G|SF\d+|HX\d+|C\d+)"
PSU_MODULAR_PATTERN = r"(?i)(?<!Non-)Modular"
PSU_COLOR_PATTERN = r"(?i)(?:\b(Black|White|Red|Blue|Green|Yellow|Gray|Grey|Orange|Purple)\b)"


def normalize_text(s: str | None) -> str | None:
    if not isinstance(s, str):
        return None

    normalized = " ".join(s.split())

    return (
        normalized.upper()
         .replace("-", " ")
         .replace("_", " ")
         .replace("/", " ")
         .replace(",", " ")
         .strip()
    )

def generate_product_id(name: str) -> str:
    return hashlib.sha1(name.encode("utf-8")).hexdigest()

def generate_product_key(spec_series: pd.Series) -> str:
    """
    Generates a unique product key based on the product's specs.
    The spec_series should contain the relevant columns for the product's specs.
    """
    # Concatenate the relevant specs into a single string
    specs_string = "|".join(spec_series.fillna("").astype(str).values.flatten())
    
    # Generate a SHA-1 hash of the concatenated specs string
    product_key = hashlib.sha1(specs_string.encode("utf-8")).hexdigest()
    
    return product_key

def generate_retailer_id(store_name: str) -> str:
    if store_name == "Newegg":
        return "newegg"
    
    return

import hashlib

CPU_NAME_PATTERN = r"(?i)^(AMD Ryzen \d \w*|Intel Core Ultra \d+ \w*|Intel Core i\d+-\d+\w*|AMD Ryzen Threadripper ?(PRO)? \d*\w*|Intel Pentium \w*)"
CPU_BRAND_PATTERN = r"(?i)^(AMD|Intel)"
CPU_SOCKET_PATTERN = r"(?i)((?:AM\d)|(?:LGA \d+)|(?:sTR\w?\d)|(?:SP\w?\d)|(?:sWRX8))"

GPU_BRAND_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+)?(\w+)"
GPU_CHIPSET_PATTERN_NVIDIA = r"(?:(?:GeForce\s?)(?:RTX|GTX|GT)?\s?(?:\d{2,4})(?:[\s-]+(?:Ti SUPER|Ti|SUPER|FE))?|RTX A\d{2,4})"
GPU_CHIPSET_PATTERN_AMD = r"(?:(?:Radeon\s?|AMD\s?)(?:RX\s|HD\s|AI Pro R)?(?:\d{2,4})(?:[\s-]+(?:XT|XTX|GRE))?|RX \d{2,4} (?:XT|XTX|GRE)?)"
GPU_CHIPSET_PATTERN_INTEL = r"(?:(?:Arc\s+)?(?:A|B)(?:\d+))"
GPU_CHIPSET_PATTERN = r"(?i)" + GPU_CHIPSET_PATTERN_NVIDIA + "|" + GPU_CHIPSET_PATTERN_AMD + "|" + GPU_CHIPSET_PATTERN_INTEL
GPU_MEMORY_PATTERN = r"(?i)((?!0)\d+\s?(?:GB|MB)|(?!0)\d+G)"
GPU_MEMORY_TYPE_PATTERN = r"(?i)(G?DDR\dX?)"

MOBO_BRAND_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+)?(\w+)"
MOBO_SOCKET_PATTERN = r"(?i)((?:AM\d)|(?:LGA\s?\d+)|(?:sTR\w?\d)|(?:SP\w?\d)|(?:sWRX8))"
MOBO_FORM_FACTOR_PATTERN = r"(?i)(Micro-ATX|mATX|Mini-ITX|ITX|ATX)"
MOBO_CHIPSET_PATTERN = r"(?i)([A-Z]\d{3}E?A?)"
MOBO_MEMORY_TYPE_PATTERN = r"(?i)(DDR\dX?)"

MEMORY_BRAND_PATTERN = r"(?i)^(?:Refurbished\s+|Open Box\s+|Memory module\s+)?((?:G.SKILL)|\w+)"
MEMORY_TYPE_PATTERN = r"(?i)(DDR\dX?)"
MEMORY_SPEED_PATTERN = r"(?i)(\b(?!DDR\d ?-?)(?:\d{4})\b|(?:\d{4}(?=MT/s))|(?:\d{4}(?=MHz)))"
MEMORY_CAPACITY_PATTERN = r"(?i)(?i)(\d+ ?GB)"
MEMORY_MODULES_PATTERN = r"(?i)(\d x \d+GB)"

STORAGE_BRAND_PATTERN = r"(?i)(?:Refurbished\s+|Open Box\s+)?(G.SKILL|Team Group|SK hynix|Western Digital|WD \w+(?: Plus| Pro)?|\w+)"
STORAGE_CAPACITY_PATTERN = r"(?i)(\d+ ?(?:GB|TB))"
STORAGE_FORM_FACTOR_PATTERN = r"(?i)(\d\.\d(?:\"|”)|\d\.\d ?-?(?:Inch|In)|M\.2(?:(?:-| )\d{2,4})?)"
STORAGE_INTERFACE_PATTERN = r"(?i)(PCI(?:e®?|-? ?Express(?: NVMe)?) (?:\d\.0|gen ?\d(?:\.0)?(?: NVMe)?)(?: ?X\d)?|m?SATA|SAS|Gen\d(?: NVMe| PCIe)|PCIe NVMe|SA510)"

PSU_BRAND_PATTERN = r"(?i)(?:Refurbished\s+|Open Box\s+|Memory module\s+)?(Lian Li|Cooler Master|Super Flower|be quiet!?|Fractal Design|Dark Power|In ?-?win|\w+)"
PSU_TYPE_PATTERN = r"(?i)(ATX|SFX(?:-L)?|TFX)"
PSU_EFFICIENCY_PATTERN = r"(?i)(80\s?(?:PLUS®?|\+)\s\w+|Cybenetics\s\w+|BRONZE|SILVER|GOLD|PLATINUM|TITANIUM)"
PSU_WATTAGE_PATTERN = r"(?i)(\d{3,}\s?W(?:att)?|RM\d+|CX\d+|SL-\d+G|SF\d+|HX\d+|C\d+)"
PSU_MODULAR_PATTERN = r"(?i)(?<!Non-)Modular"

def normalize_text(s: str | None) -> str | None:
    if not isinstance(s, str):
        return None
    return (
        s.upper()
         .replace("-", " ")
         .replace("_", " ")
         .replace("/", " ")
         .strip()
    )

def generate_product_id(name: str) -> str:
    return hashlib.sha1(name.encode("utf-8")).hexdigest()

import os
import json
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv(
    "AZURE_OPENAI_API_VERSION",
    "2024-10-21"
)


# ============================================================
# VALIDATE CONFIGURATION
# ============================================================

def validate_configuration():
    """Validate required Azure OpenAI configuration."""

    missing = []

    if not AZURE_OPENAI_ENDPOINT:
        missing.append("AZURE_OPENAI_ENDPOINT")

    if not AZURE_OPENAI_API_KEY:
        missing.append("AZURE_OPENAI_API_KEY")

    if not AZURE_OPENAI_CHAT_DEPLOYMENT:
        missing.append("AZURE_OPENAI_CHAT_DEPLOYMENT")

    if missing:
        print("\nMissing environment variables:")
        for item in missing:
            print(f"- {item}")

        print("\nPlease check your .env file.")
        return False

    return True


# ============================================================
# CREATE SEMANTIC KERNEL
# ============================================================

def create_kernel():
    """Create and configure Semantic Kernel."""

    kernel = Kernel()

    azure_chat_service = AzureChatCompletion(
        deployment_name=AZURE_OPENAI_CHAT_DEPLOYMENT,
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION
    )

    kernel.add_service(azure_chat_service)

    return kernel


# ============================================================
# PROCUREMENT DATA
# ============================================================

VENDORS = [
    {
        "name": "TechSource Solutions",
        "category": "Electronics",
        "rating": 4.7,
        "delivery_days": 7,
        "reliability": 95
    },
    {
        "name": "Global IT Supplies",
        "category": "Electronics",
        "rating": 4.4,
        "delivery_days": 10,
        "reliability": 90
    },
    {
        "name": "Enterprise Hardware Hub",
        "category": "Electronics",
        "rating": 4.2,
        "delivery_days": 14,
        "reliability": 87
    }
]


# ============================================================
# REQUEST VALIDATION
# ============================================================

def validate_request(request):
    """Validate procurement request."""

    if not request.strip():
        return False, "Procurement request cannot be empty."

    if len(request) < 20:
        return False, "Please provide more details about the procurement request."

    if len(request) > 5000:
        return False, "Procurement request is too long. Maximum 5000 characters."

    return True, ""


# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def determine_complexity(budget, quantity, urgent=False, sensitive=False):
    """
    Determine procurement complexity based on
    budget, quantity, urgency and sensitivity.
    """

    risk_score = 0

    # Budget risk
    if budget >= 1000000:
        risk_score += 3
    elif budget >= 500000:
        risk_score += 2
    elif budget >= 100000:
        risk_score += 1

    # Quantity risk
    if quantity >= 100:
        risk_score += 2
    elif quantity >= 50:
        risk_score += 1

    # Urgency risk
    if urgent:
        risk_score += 1

    # Sensitive procurement
    if sensitive:
        risk_score += 2

    # Determine complexity
    if risk_score <= 2:
        complexity = "LOW"
    elif risk_score <= 5:
        complexity = "MEDIUM"
    else:
        complexity = "HIGH"

    # Determine risk
    if risk_score <= 2:
        risk = "LOW"
    elif risk_score <= 5:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return complexity, risk, risk_score


# ============================================================
# VENDOR ANALYSIS
# ============================================================

def analyze_vendors(category="Electronics"):
    """Analyze vendors and recommend the best vendor."""

    matching_vendors = [
        vendor
        for vendor in VENDORS
        if vendor["category"].lower() == category.lower()
    ]

    if not matching_vendors:
        return None

    # Vendor scoring
    for vendor in matching_vendors:

        rating_score = vendor["rating"] / 5 * 40

        delivery_score = max(
            0,
            30 - vendor["delivery_days"]
        )

        reliability_score = vendor["reliability"] / 100 * 30

        vendor["score"] = (
            rating_score
            + delivery_score
            + reliability_score
        )

    best_vendor = max(
        matching_vendors,
        key=lambda x: x["score"]
    )

    return best_vendor


# ============================================================
# BUDGET CHECK
# ============================================================

def check_budget(budget, quantity, estimated_unit_price=50000):
    """Check whether procurement is within budget."""

    estimated_total = quantity * estimated_unit_price

    if estimated_total <= budget:
        status = "COMPLIANT"
        message = "Procurement is within the approved budget."
    else:
        status = "NON-COMPLIANT"
        message = "Estimated procurement cost exceeds the approved budget."

    return {
        "budget": budget,
        "estimated_unit_price": estimated_unit_price,
        "quantity": quantity,
        "estimated_total": estimated_total,
        "status": status,
        "message": message
    }


# ============================================================
# ADAPTIVE ORCHESTRATOR
# ============================================================

def adaptive_orchestration(
    complexity,
    risk,
    budget_status
):
    """
    Decide the workflow dynamically according
    to complexity, risk and budget compliance.
    """

    # HIGH RISK
    if complexity == "HIGH" or risk == "HIGH":

        return {
            "decision": "ESCALATE",
            "approval_required": True,
            "route": "Procurement Manager",
            "reason": (
                "High-risk or high-complexity procurement "
                "requires human approval."
            )
        }

    # BUDGET PROBLEM
    if budget_status == "NON-COMPLIANT":

        return {
            "decision": "ESCALATE",
            "approval_required": True,
            "route": "Finance + Procurement Manager",
            "reason": (
                "Procurement exceeds the approved budget."
            )
        }

    # MEDIUM COMPLEXITY
    if complexity == "MEDIUM":

        return {
            "decision": "REVIEW",
            "approval_required": True,
            "route": "Procurement Team",
            "reason": (
                "Medium-complexity procurement requires "
                "procurement review before final approval."
            )
        }

    # LOW COMPLEXITY
    return {
        "decision": "AUTO_APPROVE",
        "approval_required": False,
        "route": "Automated Procurement Workflow",
        "reason": (
            "Low-risk procurement is within budget "
            "and can be processed automatically."
        )
    }


# ============================================================
# AI PROCUREMENT ANALYSIS
# ============================================================

async def generate_ai_analysis(
    kernel,
    procurement_request,
    vendor,
    budget_info,
    complexity,
    risk,
    decision
):
    """Use Azure OpenAI through Semantic Kernel."""

    prompt = f"""
You are a Procurement Copilot.

Analyze the following procurement request.

PROCUREMENT REQUEST:
{procurement_request}

VENDOR INFORMATION:
{json.dumps(vendor, indent=2)}

BUDGET INFORMATION:
{json.dumps(budget_info, indent=2)}

COMPLEXITY:
{complexity}

RISK:
{risk}

WORKFLOW DECISION:
{json.dumps(decision, indent=2)}

Provide a concise procurement analysis.

Your response MUST contain:

1. Procurement Summary
2. Recommended Vendor
3. Vendor Reason
4. Budget Status
5. Risk Assessment
6. Workflow Decision
7. Approval Requirement
8. Recommended Next Step

Do not invent information that is not provided.
"""

    try:
        result = await kernel.invoke_prompt(
            prompt
        )

        return str(result)

    except Exception as error:
        print(f"\nAI analysis error: {error}")
        return None


# ============================================================
# PURCHASE ORDER GENERATION
# ============================================================

def generate_purchase_order(
    quantity,
    budget,
    vendor,
    procurement_request,
    budget_info,
    decision
):
    """Generate a structured purchase order."""

    estimated_total = budget_info["estimated_total"]

    purchase_order = f"""
============================================================
                    PURCHASE ORDER
============================================================

PO Number: PO-AUTO-001

------------------------------------------------------------
PROCUREMENT DETAILS
------------------------------------------------------------

Request:
{procurement_request}

Quantity:
{quantity}

------------------------------------------------------------
VENDOR DETAILS
------------------------------------------------------------

Vendor:
{vendor["name"]}

Vendor Rating:
{vendor["rating"]}/5

Expected Delivery:
{vendor["delivery_days"]} days

Reliability:
{vendor["reliability"]}%

------------------------------------------------------------
FINANCIAL DETAILS
------------------------------------------------------------

Approved Budget:
₹{budget:,.2f}

Estimated Unit Price:
₹{budget_info["estimated_unit_price"]:,.2f}

Estimated Total:
₹{estimated_total:,.2f}

Budget Status:
{budget_info["status"]}

------------------------------------------------------------
WORKFLOW
------------------------------------------------------------

Decision:
{decision["decision"]}

Approval Required:
{"YES" if decision["approval_required"] else "NO"}

Route:
{decision["route"]}

Reason:
{decision["reason"]}

============================================================
"""

    return purchase_order


# ============================================================
# SAVE PURCHASE ORDER
# ============================================================

def save_purchase_order(purchase_order):
    """Save PO to a text file."""

    try:
        with open(
            "generated_po.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(purchase_order)

        return True

    except OSError as error:
        print(f"Unable to save purchase order: {error}")
        return False


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    vendor,
    budget_info,
    complexity,
    risk,
    risk_score,
    decision,
    ai_analysis
):
    """Display procurement analysis."""

    print("\n")
    print("=" * 60)
    print("             PROCUREMENT COPILOT")
    print("=" * 60)

    print("\n[1] COMPLEXITY ANALYSIS")
    print("-" * 60)

    print(f"Complexity : {complexity}")
    print(f"Risk       : {risk}")
    print(f"Risk Score : {risk_score}")

    print("\n[2] VENDOR ANALYSIS")
    print("-" * 60)

    if vendor:
        print(f"Recommended Vendor : {vendor['name']}")
        print(f"Vendor Rating      : {vendor['rating']}/5")
        print(f"Delivery Time      : {vendor['delivery_days']} days")
        print(f"Reliability        : {vendor['reliability']}%")
        print(f"Vendor Score       : {vendor['score']:.2f}")

    print("\n[3] BUDGET CHECK")
    print("-" * 60)

    print(
        f"Approved Budget    : "
        f"₹{budget_info['budget']:,.2f}"
    )

    print(
        f"Estimated Total    : "
        f"₹{budget_info['estimated_total']:,.2f}"
    )

    print(
        f"Budget Status      : "
        f"{budget_info['status']}"
    )

    print(
        f"Message            : "
        f"{budget_info['message']}"
    )

    print("\n[4] ADAPTIVE WORKFLOW")
    print("-" * 60)

    print(f"Decision           : {decision['decision']}")
    print(
        f"Approval Required  : "
        f"{'YES' if decision['approval_required'] else 'NO'}"
    )
    print(f"Route              : {decision['route']}")
    print(f"Reason             : {decision['reason']}")

    if ai_analysis:

        print("\n[5] AI PROCUREMENT ANALYSIS")
        print("-" * 60)

        print(ai_analysis)

    print("\n" + "=" * 60)


# ============================================================
# MAIN APPLICATION
# ============================================================

async def main():
    """Main Procurement Copilot workflow."""

    print("=" * 60)
    print("       PROCUREMENT COPILOT WITH SEMANTIC KERNEL")
    print("=" * 60)

    # Validate configuration
    if not validate_configuration():
        return

    # Create kernel
    kernel = create_kernel()

    print("\nEnter procurement details.")

    procurement_request = input(
        "\nProcurement Request: "
    ).strip()

    # Validate request
    valid, message = validate_request(
        procurement_request
    )

    if not valid:
        print(f"\nInput Error: {message}")
        return

    # Collect structured information
    try:

        quantity = int(
            input("Quantity: ").strip()
        )

        budget = float(
            input("Budget (₹): ").strip()
        )

    except ValueError:

        print(
            "\nInvalid quantity or budget. "
            "Please enter numeric values."
        )

        return

    urgent_input = input(
        "Is this procurement urgent? (yes/no): "
    ).strip().lower()

    sensitive_input = input(
        "Is this a sensitive/high-risk procurement? (yes/no): "
    ).strip().lower()

    urgent = urgent_input == "yes"
    sensitive = sensitive_input == "yes"

    # --------------------------------------------------------
    # STEP 1: Complexity Analysis
    # --------------------------------------------------------

    complexity, risk, risk_score = determine_complexity(
        budget=budget,
        quantity=quantity,
        urgent=urgent,
        sensitive=sensitive
    )

    # --------------------------------------------------------
    # STEP 2: Vendor Analysis
    # --------------------------------------------------------

    vendor = analyze_vendors(
        category="Electronics"
    )

    if not vendor:

        print(
            "\nNo suitable vendor found."
        )

        return

    # --------------------------------------------------------
    # STEP 3: Budget Compliance
    # --------------------------------------------------------

    budget_info = check_budget(
        budget=budget,
        quantity=quantity,
        estimated_unit_price=50000
    )

    # --------------------------------------------------------
    # STEP 4: Adaptive Workflow
    # --------------------------------------------------------

    decision = adaptive_orchestration(
        complexity=complexity,
        risk=risk,
        budget_status=budget_info["status"]
    )

    # --------------------------------------------------------
    # STEP 5: AI Analysis
    # --------------------------------------------------------

    print("\nGenerating AI procurement analysis...")

    ai_analysis = await generate_ai_analysis(
        kernel=kernel,
        procurement_request=procurement_request,
        vendor=vendor,
        budget_info=budget_info,
        complexity=complexity,
        risk=risk,
        decision=decision
    )

    # --------------------------------------------------------
    # STEP 6: Generate Purchase Order
    # --------------------------------------------------------

    purchase_order = generate_purchase_order(
        quantity=quantity,
        budget=budget,
        vendor=vendor,
        procurement_request=procurement_request,
        budget_info=budget_info,
        decision=decision
    )

    # --------------------------------------------------------
    # STEP 7: Save PO
    # --------------------------------------------------------

    saved = save_purchase_order(
        purchase_order
    )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    display_results(
        vendor=vendor,
        budget_info=budget_info,
        complexity=complexity,
        risk=risk,
        risk_score=risk_score,
        decision=decision,
        ai_analysis=ai_analysis
    )

    print("\n[6] PURCHASE ORDER")
    print("-" * 60)

    print(purchase_order)

    if saved:
        print(
            "Purchase order saved as "
            "'generated_po.txt'"
        )

    print("\nProcurement workflow completed.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
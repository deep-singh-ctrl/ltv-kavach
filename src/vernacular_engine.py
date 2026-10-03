"""
Bharat-First Vernacular Translation & Voice Guidance Engine.
Generates plain-language, jargon-free explanations in Hindi and English for Tier-2/3 investors.
"""

from typing import Dict, Any

def generate_vernacular_guidance(analysis_data: Dict[str, Any], lang: str = "hi") -> Dict[str, str]:
    """
    Produces concise, clear guidance in Hindi and English.
    """
    ltv_pct = analysis_data.get("current_ltv_pct", 50.0)
    drop_pct = analysis_data.get("drop_to_margin_call_pct", 0.0)
    zone = analysis_data.get("status_zone", "SAFE_GREEN")
    remedies = analysis_data.get("remedies", {})
    cash_fix = remedies.get("cash_prepayment_remedy", {}).get("amount_inr", 0.0)
    debt_fix = remedies.get("pledge_collateral_remedy", {}).get("amount_inr", 0.0)

    if lang == "hi":
        # Hindi guidance
        if zone == "SAFE_GREEN":
            title = "स्थिति सुरक्षित है (Safe Zone)"
            message = (
                f"आपके गिरवी रखे शेयर सुरक्षित हैं। वर्तमान LTV {ltv_pct}% है। "
                f"बाज़ार में {drop_pct}% तक की गिरावट आने पर भी आपके शेयरों पर कोई खतरा नहीं है।"
            )
            action_prompt = "किसी अतिरिक्त भुगतान की आवश्यकता नहीं है। आराम से निवेश जारी रखें।"
            speech_text = (
                f"नमस्ते। आपका लोन सुरक्षित है। वर्तमान एलटीवी {ltv_pct} प्रतिशत है। "
                f"बाज़ार {drop_pct} प्रतिशत गिरने पर भी बैंक आपके शेयर नहीं बेचेगा।"
            )
        elif zone == "MODERATE_YELLOW":
            title = "सतर्क रहें (Caution Zone)"
            message = (
                f"सावधान! आपका LTV {ltv_pct}% पर पहुँच गया है। यदि बाज़ार {drop_pct}% और गिरता है, "
                f"तो बैंक मार्जिन कॉल भेज देगा।"
            )
            action_prompt = f"लोन को पूरी तरह सुरक्षित करने के लिए ₹{round(cash_fix):,} का भुगतान करें या सुरक्षित डेट फंड जोड़ें।"
            speech_text = (
                f"ध्यान दें। आपका लोन पीली यानी सतर्क श्रेणी में है। "
                f"अगर बाज़ार {drop_pct} प्रतिशत गिरता है, तो बैंक मार्जिन कॉल देगा। "
                f"सुरक्षा के लिए ₹{round(cash_fix):,} चुकाएं।"
            )
        else: # WARNING_AMBER or CRITICAL_RED
            title = "अति गंभीर चेतावनी: शेयर बिकने का खतरा! (Danger Zone)"
            message = (
                f"खतरा! LTV सीमा पार हो चुकी है ({ltv_pct}%)। बैंक तुरंत आपके गिरवी रखे शेयर "
                f"बाज़ार में कम कीमत पर बेच सकता है।"
            )
            action_prompt = (
                f"तुरंत ₹{round(cash_fix):,} का बैंक भुगतान करें या ₹{round(debt_fix):,} "
                f"का सुरक्षित लिक्विड फंड गिरवी रखकर अपने शेयरों को बचाएं।"
            )
            speech_text = (
                f"गंभीर चेतावनी! आपके शेयर बिकने का खतरा है। "
                f"बैंक को तुरंत ₹{round(cash_fix):,} का भुगतान करें अथवा अतिरिक्त सुरक्षित फंड जोड़ें।"
            )

        return {
            "lang": "hi",
            "lang_name": "हिंदी (Hindi)",
            "title": title,
            "message": message,
            "action_prompt": action_prompt,
            "speech_text": speech_text
        }

    else:
        # English guidance
        if zone == "SAFE_GREEN":
            title = "Loan Collateral is Safe & Resilient"
            message = (
                f"Your pledged investments are safe with an LTV of {ltv_pct}%. "
                f"The market would need to fall by more than {drop_pct}% before any margin action occurs."
            )
            action_prompt = "No defensive action required. Maintain your normal savings schedule."
            speech_text = (
                f"Your loan collateral is in the safe zone with an LTV of {ltv_pct} percent. "
                f"You have a healthy {drop_pct} percent buffer before any margin warning."
            )
        elif zone == "MODERATE_YELLOW":
            title = "Caution: Collateral Buffer Narrowing"
            message = (
                f"Attention: Your LTV has risen to {ltv_pct}%. A market correction of just {drop_pct}% "
                f"will trigger an urgent margin call from your lender."
            )
            action_prompt = f"Recommended: Prepay ₹{round(cash_fix):,} or pledge low-risk debt funds to shockproof your position."
            speech_text = (
                f"Attention. Your loan buffer is narrowing. An additional market dip of {drop_pct} percent "
                f"will trigger a margin call. Consider adding a small safety buffer."
            )
        else:
            title = "Critical Alert: Forced Liquidation Risk!"
            message = (
                f"Danger: Your LTV is {ltv_pct}%, breaching safe limits. The lender is legally entitled "
                f"to sell off your pledged shares at current market prices."
            )
            action_prompt = (
                f"Immediate Action: Pay ₹{round(cash_fix):,} cash or pledge ₹{round(debt_fix):,} "
                f"of safe liquid securities to prevent distress liquidation."
            )
            speech_text = (
                f"Critical alert! Your pledged portfolio is in the danger zone. "
                f"To prevent lender liquidation, pay ₹{round(cash_fix):,} immediately or pledge additional collateral."
            )

        return {
            "lang": "en",
            "lang_name": "English",
            "title": title,
            "message": message,
            "action_prompt": action_prompt,
            "speech_text": speech_text
        }

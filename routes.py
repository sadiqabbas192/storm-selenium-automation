from fastapi import FastAPI, HTTPException
from all_func import run_storm_automation

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Define endpoint for automation
@app.get("/get_article/")
def generate_summary(title_str: str, response_str: str):
    """Runs STORM automation and returns extracted summary text."""
    try:
        print(f"🔹 Received Request: Title: {title_str} | Response: {response_str}")
        extracted_text = run_storm_automation(title_str, response_str)
        
        # if not extracted_text:
        #     raise HTTPException(status_code=500, detail="Automation failed. No text extracted.")
        
        return {"title": title_str,
                "response": response_str,
                "summary": extracted_text}

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
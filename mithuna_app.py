import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types
import markdown

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyCtV_mwWwZw7QbP01RqSxRGiFXSptJiPak")

@app.route('/')
def home():
    disclaimer_text = "PorePal is an educational tool and not a replacement for professional dermatological diagnosis."
    return render_template('index.html', medical_note=disclaimer_text)

@app.route('/upload-page', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        uploaded_file = request.files.get('skin_image')
        
        if uploaded_file and uploaded_file.filename != '':
            try:
                image_bytes = uploaded_file.read()
                
                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=uploaded_file.content_type
                )
                
                prompt = (
                    "Analyze this skin/skincare photo for educational purposes. "
                    "Identify the general visible skin characteristics (like dry, oily, or normal areas). "
                    "Provide 3 basic, gentle, everyday skincare routine tips tailored to this observation. "
                    "Keep your response strictly informative and include a reminder to consult a professional."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image_part, prompt]
                )

                formatted_html_text = markdown.markdown(response.text)
                
                return f"""
                <body style="font-family: sans-serif; background: #e3f2fd; padding: 50px; text-align: center;">
                    <div style="background: white; border-radius: 20px; padding: 40px; display: inline-block; text-align: left; max-width: 600px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                        <h2>✨ PorePal AI Analysis Results</h2>
                        <hr>
                        <div style="line-height: 1.6; white-space: pre-wrap;">{formatted_html_text}</div>
                        <hr>
                        <a href="/" style="text-decoration: none; color: #89cff0; font-weight: bold;">← Go Back to Dashboard</a>
                    </div>
                </body>
                """
            except Exception as e:
                return f"An error occurred while talking to Gemini AI: {str(e)}"
                
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai # Du trenger en API-nøkkel fra OpenAI eller tilsvarende

# --- KONFIGURASJON ---
# Erstatt disse med dine egne verdier eller miljøvariabler
OPENAI_API_KEY = "DIN_API_NØKKEL_HER"
AVSENDER_EPOST = "frodo@venstre.no"
AVSENDER_PASSORD = "fdhv orfh uzgk tuqg" # Bruk "App Password" hvis du bruker Gmail
MOTTAKER_EPOST = "frode.nergaard.fjeldstad@spv.no"

KILDER = {
    "Politico EU": "https://www.politico.eu/section/policy/feed/",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "Aftenposten": "https://www.aftenposten.no/rss",
    "CNN": "http://rss.cnn.com/rss/edition_world.rss"
}

def hent_og_filtrer_nyheter():
    nyhets_data = ""
    for navn, url in KILDER.items():
        feed = feedparser.parse(url)
        nyhets_data += f"\n--- KILDE: {navn} ---\n"
        # Henter de 5 nyeste fra hver
        for entry in feed.entries[:5]:
            nyhets_data += f"Tittel: {entry.title}\nSammendrag: {entry.get('summary', 'Ingen beskrivelse')}\n\n"
    return nyhets_data

def generer_nyhetsbrev_med_ai(raadata):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""
    Du er en senior analytiker innen internasjonal politikk. 
    Basert på følgende nyhetsstrøm, lag et kortfattet og profesjonelt nyhetsbrev for Frode.
    
    Regler:
    1. Velg ut de 5 viktigste sakene globalt.
    2. Forklar den geopolitiske betydningen for hver sak.
    3. Hvis flere kilder skriver om det samme, slå det sammen.
    4. Språk: Norsk.
    
    NYHETER:
    {raadata}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def send_epost(innhold):
    msg = MIMEMultipart()
    msg['From'] = AVSENDER_EPOST
    msg['To'] = MOTTAKER_EPOST
    msg['Subject'] = "Morgenbrief: Internasjonal Politikk"

    msg.attach(MIMEText(innhold, 'plain'))

    # Eksempel for Gmail-oppsett
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(AVSENDER_EPOST, AVSENDER_PASSORD)
    server.send_message(msg)
    server.quit()

# --- HOVEDKJØRING ---
if __name__ == "__main__":
    print("Henter nyheter...")
    data = hent_og_filtrer_nyheter()
    print("Analyserer med AI...")
    brief = generer_nyhetsbrev_med_ai(data)
    print(f"Sender e-post til {MOTTAKER_EPOST}...")
    send_epost(brief)
    print("Ferdig!")

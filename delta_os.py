"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              DELTA OS v1.0                                   ║
║           Digital Enhanced Logical Thinking Assistant                        ║
║                                                                              ║
║                      Créé pour Monsieur Sezer                                ║
║                                                                              ║
║  Architecture Cognitive Avancée avec Sécurité Multi-Niveaux                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import os
from datetime import datetime
import json
import hashlib
from typing import Dict, List, Optional, Any
import subprocess
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 : CONFIGURATION GLOBALE
# ═══════════════════════════════════════════════════════════════════════════════

MASTER_CODE = "B2008a2020@"
AUTHORIZED_IP = "82.64.93.65"
LOCATION = "Annecy, Rhône-Alpes, FR"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 : GESTION DE SUPABASE
# ═══════════════════════════════════════════════════════════════════════════════

class SupabaseManager:
    """Gestionnaire de connexion et opérations Supabase"""
    
    def __init__(self):
        """Initialisation de la connexion Supabase"""
        try:
            from supabase import create_client, Client
            self.supabase_url = st.secrets.get("SUPABASE_URL", "")
            self.supabase_key = st.secrets.get("SUPABASE_KEY", "")
            self.client: Optional[Client] = None
            
            if self.supabase_url and self.supabase_key:
                try:
                    self.client = create_client(self.supabase_url, self.supabase_key)
                    st.success("✅ Connexion Supabase établie")
                except Exception as e:
                    st.error(f"❌ Erreur connexion Supabase: {e}")
            else:
                st.warning("⚠️ Clés Supabase non configurées")
        except ImportError:
            st.error("❌ Module 'supabase' non installé. Installez-le avec: pip install supabase")
            self.client = None
    
    def is_connected(self) -> bool:
        """Vérifie si la connexion est établie"""
        return self.client is not None
    
    def insert(self, table: str, data: Dict) -> bool:
        """Insère un enregistrement dans une table"""
        if not self.is_connected():
            st.error("❌ Pas de connexion Supabase")
            return False
        
        try:
            self.client.table(table).insert(data).execute()
            return True
        except Exception as e:
            st.error(f"❌ Erreur insertion dans {table}: {e}")
            return False
    
    def select(self, table: str, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """Sélectionne des enregistrements d'une table"""
        if not self.is_connected():
            return []
        
        try:
            query = self.client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"❌ Erreur lecture {table}: {e}")
            return []

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 : SYSTÈME DE SÉCURITÉ
# ═══════════════════════════════════════════════════════════════════════════════

class SecurityLayer:
    """Couche de sécurité pour toutes les actions sensibles"""
    
    @staticmethod
    def verify_code(input_code: str) -> bool:
        """Vérifie le code maître"""
        return input_code == MASTER_CODE
    
    @staticmethod
    def request_auth(action_name: str, key_suffix: str = "") -> bool:
        """
        Demande une autorisation pour une action sensible
        
        Args:
            action_name: Nom de l'action (ex: "envoi email")
            key_suffix: Suffixe unique pour le widget (évite les doublons)
        
        Returns:
            True si autorisé, False sinon
        """
        st.warning(f"🔐 Action sensible : **{action_name}**")
        st.info("⚠️ Code maître requis pour continuer")
        
        # Génération d'une clé unique pour le widget
        widget_key = f"auth_{action_name}_{key_suffix}_{datetime.now().timestamp()}"
        
        code_input = st.text_input(
            "Entrez le code maître",
            type="password",
            key=widget_key,
            help="Code configuré dans le système"
        )
        
        if code_input:
            if SecurityLayer.verify_code(code_input):
                st.success("✅ Code correct - Action autorisée")
                return True
            else:
                st.error("❌ Code incorrect - Action refusée")
                return False
        
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 : SYSTÈME DE MÉMOIRE COGNITIVE
# ═══════════════════════════════════════════════════════════════════════════════

class MemorySystem:
    """Système de mémoire quadruple de DELTA"""
    
    def __init__(self, db: SupabaseManager):
        """
        Initialisation du système de mémoire
        
        Args:
            db: Instance du gestionnaire Supabase
        """
        self.db = db
    
    # ───────────────────────────────────────────────────────────────────────────
    # MÉMOIRE SÉMANTIQUE - Faits permanents
    # ───────────────────────────────────────────────────────────────────────────
    
    def store_semantic(self, category: str, key: str, value: str) -> bool:
        """
        Stocke un fait permanent
        
        Args:
            category: Catégorie du fait (Personnel, Projet, Contact, Préférence)
            key: Clé unique du fait
            value: Valeur du fait
        
        Returns:
            True si succès, False sinon
        """
        data = {
            "category": category,
            "key": key,
            "value": value,
            "created_at": datetime.now().isoformat()
        }
        return self.db.insert("semantic_memory", data)
    
    def get_semantic(self, category: Optional[str] = None) -> List[Dict]:
        """
        Récupère les faits permanents
        
        Args:
            category: Filtre optionnel par catégorie
        
        Returns:
            Liste des faits
        """
        filters = {"category": category} if category else None
        return self.db.select("semantic_memory", filters)
    
    # ───────────────────────────────────────────────────────────────────────────
    # MÉMOIRE ÉPISODIQUE - Historique des interactions
    # ───────────────────────────────────────────────────────────────────────────
    
    def log_interaction(self, interaction_type: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """
        Enregistre une interaction dans l'historique
        
        Args:
            interaction_type: Type d'interaction (conversation, action, etc.)
            content: Contenu de l'interaction
            metadata: Métadonnées additionnelles
        
        Returns:
            True si succès, False sinon
        """
        data = {
            "interaction_type": interaction_type,
            "content": content,
            "metadata": json.dumps(metadata) if metadata else "{}",
            "timestamp": datetime.now().isoformat()
        }
        return self.db.insert("episodic_memory", data)
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """
        Récupère l'historique des interactions
        
        Args:
            limit: Nombre maximum d'interactions à récupérer
        
        Returns:
            Liste des interactions
        """
        return self.db.select("episodic_memory", limit=limit)
    
    # ───────────────────────────────────────────────────────────────────────────
    # MÉMOIRE PROCÉDURALE - Habitudes et routines
    # ───────────────────────────────────────────────────────────────────────────
    
    def store_habit(self, action: str, frequency: int, context: str) -> bool:
        """
        Enregistre une habitude ou routine
        
        Args:
            action: Description de l'action
            frequency: Fréquence d'exécution
            context: Contexte de l'action
        
        Returns:
            True si succès, False sinon
        """
        data = {
            "action": action,
            "frequency": frequency,
            "context": context,
            "last_executed": datetime.now().isoformat()
        }
        return self.db.insert("procedural_memory", data)
    
    def get_habits(self) -> List[Dict]:
        """
        Récupère les habitudes enregistrées
        
        Returns:
            Liste des habitudes
        """
        return self.db.select("procedural_memory")
    
    # ───────────────────────────────────────────────────────────────────────────
    # MÉMOIRE DE TRAVAIL - Contexte de session
    # ───────────────────────────────────────────────────────────────────────────
    
    def set_context(self, key: str, value: Any) -> None:
        """
        Stocke une valeur dans le contexte de session
        
        Args:
            key: Clé de la valeur
            value: Valeur à stocker
        """
        if "work_memory" not in st.session_state:
            st.session_state.work_memory = {}
        st.session_state.work_memory[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur du contexte de session
        
        Args:
            key: Clé de la valeur
            default: Valeur par défaut si non trouvée
        
        Returns:
            Valeur stockée ou default
        """
        if "work_memory" not in st.session_state:
            st.session_state.work_memory = {}
        return st.session_state.work_memory.get(key, default)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 : MODULE DE PERCEPTION
# ═══════════════════════════════════════════════════════════════════════════════

class PerceptionModule:
    """Module de perception de l'environnement"""
    
    @staticmethod
    def get_time() -> Dict[str, str]:
        """
        Retourne l'heure et la date actuelles
        
        Returns:
            Dictionnaire avec date, heure, jour
        """
        now = datetime.now()
        return {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "iso": now.isoformat()
        }
    
    @staticmethod
    def get_location() -> Dict[str, str]:
        """
        Retourne la localisation
        
        Returns:
            Dictionnaire avec ville, région, pays
        """
        return {
            "city": "Annecy",
            "region": "Rhône-Alpes",
            "country": "France",
            "full": LOCATION
        }
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """
        Retourne les informations système
        
        Returns:
            Dictionnaire avec OS, version, architecture
        """
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 : MODULE DE COMMUNICATION
# ═══════════════════════════════════════════════════════════════════════════════

class CommunicationModule:
    """Module de gestion des communications (Email)"""
    
    def __init__(self):
        """Initialisation avec configuration email depuis secrets"""
        self.smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(st.secrets.get("SMTP_PORT", 587))
        self.imap_server = st.secrets.get("IMAP_SERVER", "imap.gmail.com")
        self.email_address = st.secrets.get("EMAIL_ADDRESS", "")
        self.email_password = st.secrets.get("EMAIL_PASSWORD", "")
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Envoie un email (NÉCESSITE AUTORISATION)
        
        Args:
            to: Destinataire
            subject: Sujet de l'email
            body: Corps de l'email
        
        Returns:
            True si envoyé, False sinon
        """
        if not self.email_address or not self.email_password:
            st.error("❌ Configuration email manquante dans les secrets")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            
            st.success(f"✅ Email envoyé à {to}")
            return True
            
        except Exception as e:
            st.error(f"❌ Erreur envoi email: {e}")
            return False
    
    def read_inbox(self, max_emails: int = 10) -> List[Dict]:
        """
        Lit les emails de la boîte de réception (NÉCESSITE AUTORISATION)
        
        Args:
            max_emails: Nombre maximum d'emails à lire
        
        Returns:
            Liste des emails
        """
        if not self.email_address or not self.email_password:
            st.error("❌ Configuration email manquante dans les secrets")
            return []
        
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_address, self.email_password)
            mail.select('inbox')
            
            _, messages = mail.search(None, 'ALL')
            email_ids = messages[0].split()
            
            emails = []
            for email_id in email_ids[-max_emails:]:
                _, msg_data = mail.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                emails.append({
                    "from": email_message.get('From', 'Inconnu'),
                    "subject": email_message.get('Subject', 'Sans sujet'),
                    "date": email_message.get('Date', 'Date inconnue')
                })
            
            mail.close()
            mail.logout()
            
            st.success(f"✅ {len(emails)} email(s) récupéré(s)")
            return emails
            
        except Exception as e:
            st.error(f"❌ Erreur lecture emails: {e}")
            return []

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 : MODULE SYSTÈME
# ═══════════════════════════════════════════════════════════════════════════════

class SystemModule:
    """Module d'interaction avec le système d'exploitation"""
    
    @staticmethod
    def execute_command(command: str) -> Dict[str, Any]:
        """
        Exécute une commande système (NÉCESSITE AUTORISATION)
        
        Args:
            command: Commande à exécuter
        
        Returns:
            Dictionnaire avec succès, sortie, erreur
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            
            if success:
                st.success(f"✅ Commande exécutée avec succès")
            else:
                st.error(f"❌ Commande échouée (code {result.returncode})")
            
            return {
                "success": success,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            st.error("❌ Timeout : la commande a pris trop de temps")
            return {
                "success": False,
                "output": "",
                "error": "Timeout dépassé (30s)",
                "return_code": -1
            }
        except Exception as e:
            st.error(f"❌ Erreur exécution : {e}")
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }
    
    @staticmethod
    def list_directory(path: str = ".") -> List[str]:
        """
        Liste les fichiers d'un répertoire
        
        Args:
            path: Chemin du répertoire
        
        Returns:
            Liste des fichiers
        """
        try:
            files = os.listdir(path)
            st.success(f"✅ {len(files)} fichier(s) trouvé(s)")
            return files
        except Exception as e:
            st.error(f"❌ Erreur lecture répertoire: {e}")
            return []

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 : CERVEAU DELTA (ORCHESTRATEUR PRINCIPAL)
# ═══════════════════════════════════════════════════════════════════════════════

class DELTA:
    """Intelligence Artificielle Cognitive - Système de Supervision"""
    
    def __init__(self):
        """Initialisation de tous les modules de DELTA"""
        self.name = "DELTA"
        self.db = SupabaseManager()
        self.memory = MemorySystem(self.db)
        self.perception = PerceptionModule()
        self.communication = CommunicationModule()
        self.system = SystemModule()
        self.security = SecurityLayer()
    
    def greet_user(self) -> str:
        """
        Génère une salutation personnalisée
        
        Returns:
            Message de salutation
        """
        time_info = self.perception.get_time()
        hour = int(datetime.now().strftime("%H"))
        
        if 5 <= hour < 12:
            greeting = "Bonjour"
        elif 12 <= hour < 18:
            greeting = "Bon après-midi"
        else:
            greeting = "Bonsoir"
        
        return f"{greeting}, Monsieur Sezer. DELTA est opérationnel et à votre service."
    
    def process_command(self, command: str) -> str:
        """
        Traite une commande utilisateur
        
        Args:
            command: Commande saisie par l'utilisateur
        
        Returns:
            Réponse de DELTA
        """
        command_lower = command.lower()
        
        # Commande : Heure et date
        if any(word in command_lower for word in ["heure", "date", "jour"]):
            info = self.perception.get_time()
            return f"Nous sommes le **{info['day']} {info['date']}** et il est **{info['time']}**, Monsieur Sezer."
        
        # Commande : Localisation
        elif any(word in command_lower for word in ["où", "localisation", "position"]):
            loc = self.perception.get_location()
            return f"Vous êtes à **{loc['full']}**, Monsieur Sezer."
        
        # Commande : Informations système
        elif any(word in command_lower for word in ["système", "info", "ordinateur"]):
            sys_info = self.perception.get_system_info()
            return f"**Système** : {sys_info['os']} {sys_info['os_version']}\n**Architecture** : {sys_info['architecture']}\n**Python** : {sys_info['python_version']}"
        
        # Commande : Salutation
        elif any(word in command_lower for word in ["bonjour", "salut", "hello", "hey"]):
            return self.greet_user()
        
        # Commande non reconnue
        else:
            return "Je n'ai pas compris votre commande, Monsieur Sezer. Essayez : 'quelle heure est-il ?', 'où suis-je ?' ou 'info système'."
    
    def log_interaction(self, user_input: str, delta_response: str) -> None:
        """
        Enregistre l'interaction dans la mémoire épisodique
        
        Args:
            user_input: Entrée utilisateur
            delta_response: Réponse de DELTA
        """
        self.memory.log_interaction(
            interaction_type="conversation",
            content=user_input,
            metadata={"response": delta_response}
        )

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9 : INTERFACE UTILISATEUR STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale de l'application Streamlit"""
    
    # ───────────────────────────────────────────────────────────────────────────
    # Configuration de la page
    # ───────────────────────────────────────────────────────────────────────────
    
    st.set_page_config(
        page_title="DELTA OS",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # ───────────────────────────────────────────────────────────────────────────
    # Initialisation de DELTA dans session_state
    # ───────────────────────────────────────────────────────────────────────────
    
    if "delta" not in st.session_state:
        st.session_state.delta = DELTA()
    
    delta = st.session_state.delta
    
    # ───────────────────────────────────────────────────────────────────────────
    # SIDEBAR - Informations et Navigation
    # ───────────────────────────────────────────────────────────────────────────
    
    with st.sidebar:
        st.title("⚙️ DELTA OS")
        st.caption("Digital Enhanced Logical Thinking Assistant")
        st.caption("Version 1.0 - Créé pour Monsieur Sezer")
        
        st.divider()
        
        # État du système
        st.subheader("📊 État du Système")
        time_info = delta.perception.get_time()
        st.metric("📅 Date", time_info['date'])
        st.metric("🕐 Heure", time_info['time'])
        
        st.divider()
        
        # Statut connexions
        st.subheader("🔌 Connexions")
        if delta.db.is_connected():
            st.success("✅ Supabase")
        else:
            st.error("❌ Supabase")
        
        st.divider()
        
        # Navigation
        st.subheader("🧭 Navigation")
        page = st.radio(
            "Sélectionnez un module",
            ["💬 Conversation", "🧠 Mémoire", "📧 Communication", "⚙️ Système", "🔧 Paramètres"],
            label_visibility="collapsed"
        )
    
    # ───────────────────────────────────────────────────────────────────────────
    # HEADER PRINCIPAL
    # ───────────────────────────────────────────────────────────────────────────
    
    st.title("🤖 DELTA - Digital Enhanced Logical Thinking Assistant")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 1 : CONVERSATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    if page == "💬 Conversation":
        st.header("💬 Interface de Conversation")
        
        # Message de bienvenue (une seule fois)
        if "greeted" not in st.session_state:
            st.info(delta.greet_user())
            st.session_state.greeted = True
        
        # Initialisation de l'historique de conversation
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        
        # Affichage de l'historique
        for msg in st.session_state.conversation_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(f"**Monsieur Sezer** : {msg['content']}")
            else:
                with st.chat_message("assistant"):
                    st.write(f"**DELTA** : {msg['content']}")
        
        # Input utilisateur
        user_input = st.chat_input("Votre commande, Monsieur Sezer...")
        
        if user_input:
            # Ajouter le message utilisateur
            st.session_state.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Traiter la commande
            response = delta.process_command(user_input)
            
            # Ajouter la réponse de DELTA
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Logger l'interaction
            delta.log_interaction(user_input, response)
            
            # Rafraîchir pour afficher
            st.rerun()
        
        # Instructions
        with st.expander("ℹ️ Commandes disponibles"):
            st.markdown("""
            **Commandes de base :**
            - `quelle heure est-il ?` → Affiche la date et l'heure
            - `où suis-je ?` → Affiche votre localisation
            - `info système` → Affiche les informations système
            - `bonjour` → Salutation personnalisée
            """)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 2 : MÉMOIRE
    # ═══════════════════════════════════════════════════════════════════════════
    
    elif page == "🧠 Mémoire":
        st.header("🧠 Système de Mémoire Cognitive")
        
        tab1, tab2, tab3 = st.tabs(["📚 Sémantique", "📜 Épisodique", "🔄 Procédurale"])
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 1 : Mémoire Sémantique
        # ─────────────────────────────────────────────────────────────────────
        
        with tab1:
            st.subheader("📚 Mémoire Sémantique - Faits Permanents")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### ➕ Ajouter un Fait")
                
                category = st.selectbox(
                    "Catégorie",
                    ["Personnel", "Projet", "Contact", "Préférence"],
                    help="Type de fait à enregistrer"
                )
                
                key = st.text_input(
                    "Clé",
                    placeholder="Ex: email_principal",
                    help="Identifiant unique du fait"
                )
                
                value = st.text_area(
                    "Valeur",
                    placeholder="Ex: sezer@example.com",
                    help="Contenu du fait"
                )
                
                if st.button("💾 Enregistrer le Fait", type="primary"):
                    if key and value:
                        success = delta.memory.store_semantic(category, key, value)
                        if success:
                            st.success(f"✅ Fait '{key}' enregistré avec succès !")
                            st.balloons()
                        else:
                            st.error("❌ Erreur lors de l'enregistrement")
                    else:
                        st.warning("⚠️ Veuillez remplir la clé et la valeur")
            
            with col2:
                st.markdown("### 📋 Faits Stockés")
                
                # Filtrage par catégorie
                filter_category = st.selectbox(
                    "Filtrer par catégorie",
                    ["Toutes", "Personnel", "Projet", "Contact", "Préférence"],
                    key="filter_semantic"
                )
                
                # Récupération des faits
                if filter_category == "Toutes":
                    facts = delta.memory.get_semantic()
                else:
                    facts = delta.memory.get_semantic(filter_category)
                
                # Affichage
                if facts:
                    st.info(f"📊 **{len(facts)} fait(s)** trouvé(s)")
                    for fact in facts:
                        with st.container():
                            st.markdown(f"""
                            **Catégorie** : `{fact.get('category', 'N/A')}`  
                            **Clé** : `{fact.get('key', 'N/A')}`  
                            **Valeur** : {fact.get('value', 'N/A')}  
                            *Créé le : {fact.get('created_at', 'N/A')}*
                            """)
                            st.divider()
                else:
                    st.warning("Aucun fait enregistré pour le moment")
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 2 : Mémoire Épisodique
        # ─────────────────────────────────────────────────────────────────────
        
        with tab2:
            st.subheader("📜 Mémoire Épisodique - Historique des Interactions")
            
            # Récupération de l'historique
            history = delta.memory.get_history(limit=50)
            
            if history:
                st.info(f"📊 **{len(history)} interaction(s)** enregistrée(s)")
                
                # Affichage sous forme de timeline
                for entry in reversed(history):  # Ordre chronologique inverse
                    timestamp = entry.get('timestamp', 'N/A')
                    interaction_type = entry.get('interaction_type', 'N/A')
                    content = entry.get('content', 'N/A')
                    
                    with st.container():
                        st.markdown(f"""
                        **⏰ {timestamp}** | Type : `{interaction_type}`  
                        💬 {content}
                        """)
                        st.divider()
            else:
                st.warning("Aucune interaction enregistrée pour le moment")
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 3 : Mémoire Procédurale
        # ─────────────────────────────────────────────────────────────────────
        
        with tab3:
            st.subheader("🔄 Mémoire Procédurale - Habitudes et Routines")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### ➕ Ajouter une Habitude")
                
                action = st.text_input(
                    "Action",
                    placeholder="Ex: Vérifier les emails",
                    help="Description de l'action répétitive"
                )
                
                frequency = st.number_input(
                    "Fréquence (fois/semaine)",
                    min_value=1,
                    max_value=100,
                    value=7,
                    help="Nombre de fois par semaine"
                )
                
                context = st.text_area(
                    "Contexte",
                    placeholder="Ex: Tous les matins à 9h",
                    help="Dans quel contexte cette action est effectuée"
                )
                
                if st.button("💾 Enregistrer l'Habitude", type="primary"):
                    if action and context:
                        success = delta.memory.store_habit(action, frequency, context)
                        if success:
                            st.success(f"✅ Habitude '{action}' enregistrée !")
                        else:
                            st.error("❌ Erreur lors de l'enregistrement")
                    else:
                        st.warning("⚠️ Veuillez remplir l'action et le contexte")
            
            with col2:
                st.markdown("### 📋 Habitudes Stockées")
                
                # Récupération des habitudes
                habits = delta.memory.get_habits()
                
                if habits:
                    st.info(f"📊 **{len(habits)} habitude(s)** enregistrée(s)")
                    for habit in habits:
                        with st.container():
                            st.markdown(f"""
                            **🎯 Action** : {habit.get('action', 'N/A')}  
                            **📈 Fréquence** : {habit.get('frequency', 0)} fois/semaine  
                            **📝 Contexte** : {habit.get('context', 'N/A')}  
                            *Dernière exécution : {habit.get('last_executed', 'N/A')}*
                            """)
                            st.divider()
                else:
                    st.warning("Aucune habitude enregistrée pour le moment")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 3 : COMMUNICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    elif page == "📧 Communication":
        st.header("📧 Module de Communication")
        
        tab1, tab2 = st.tabs(["✉️ Envoyer Email", "📬 Lire Inbox"])
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 1 : Envoi d'email
        # ─────────────────────────────────────────────────────────────────────
        
        with tab1:
            st.subheader("✉️ Envoi d'Email Sécurisé")
            
            # Formulaire d'envoi
            with st.form("email_form"):
                to = st.text_input(
                    "📧 Destinataire",
                    placeholder="exemple@email.com",
                    help="Adresse email du destinataire"
                )
                
                subject = st.text_input(
                    "📝 Sujet",
                    placeholder="Objet de l'email",
                    help="Sujet de l'email"
                )
                
                body = st.text_area(
                    "💬 Message",
                    placeholder="Contenu de votre email...",
                    height=200,
                    help="Corps de l'email"
                )
                
                submitted = st.form_submit_button("📤 Demander l'Envoi", type="primary")
            
            # Traitement de l'envoi
            if submitted:
                if to and subject and body:
                    # Demande d'autorisation
                    st.markdown("---")
                    if delta.security.request_auth("Envoi Email", "send_email"):
                        # Envoi de l'email
                        success = delta.communication.send_email(to, subject, body)
                        if success:
                            # Logger l'action
                            delta.memory.log_interaction(
                                "email_sent",
                                f"Email envoyé à {to}",
                                {"subject": subject}
                            )
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs")
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 2 : Lecture inbox
        # ─────────────────────────────────────────────────────────────────────
        
        with tab2:
            st.subheader("📬 Lecture de la Boîte de Réception")
            
            max_emails = st.slider(
                "Nombre d'emails à récupérer",
                min_value=1,
                max_value=50,
                value=10,
                help="Nombre maximum d'emails à afficher"
            )
            
            if st.button("📥 Lire les Emails", type="primary"):
                # Demande d'autorisation
                st.markdown("---")
                if delta.security.request_auth("Lecture Emails", "read_inbox"):
                    # Lecture des emails
                    emails = delta.communication.read_inbox(max_emails)
                    
                    if emails:
                        st.success(f"✅ {len(emails)} email(s) récupéré(s)")
                        
                        # Affichage des emails
                        for i, email_data in enumerate(emails, 1):
                            with st.expander(f"📧 Email {i} : {email_data.get('subject', 'Sans sujet')}"):
                                st.markdown(f"""
                                **De** : {email_data.get('from', 'Inconnu')}  
                                **Sujet** : {email_data.get('subject', 'Sans sujet')}  
                                **Date** : {email_data.get('date', 'Date inconnue')}
                                """)
                        
                        # Logger l'action
                        delta.memory.log_interaction(
                            "inbox_read",
                            f"{len(emails)} emails lus",
                            {"max_emails": max_emails}
                        )
                    else:
                        st.info("Aucun email trouvé ou erreur de connexion")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 4 : SYSTÈME
    # ═══════════════════════════════════════════════════════════════════════════
    
    elif page == "⚙️ Système":
        st.header("⚙️ Module Système")
        
        tab1, tab2 = st.tabs(["💻 Exécution Commande", "📁 Navigation Fichiers"])
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 1 : Exécution de commande
        # ─────────────────────────────────────────────────────────────────────
        
        with tab1:
            st.subheader("💻 Exécution de Commande Système")
            
            st.warning("⚠️ **Attention** : L'exécution de commandes système peut être dangereuse. Utilisez avec précaution.")
            
            # Input commande
            command = st.text_input(
                "Commande à exécuter",
                placeholder="Ex: echo 'Hello DELTA'",
                help="Commande shell à exécuter"
            )
            
            # Exemples de commandes
            with st.expander("📖 Exemples de commandes sûres"):
                st.markdown("""
                **Linux/Mac** :
                - `echo "Hello DELTA"` → Affiche un message
                - `pwd` → Affiche le répertoire actuel
                - `ls -la` → Liste les fichiers
                - `date` → Affiche la date
                
                **Windows** :
                - `echo Hello DELTA` → Affiche un message
                - `cd` → Affiche le répertoire actuel
                - `dir` → Liste les fichiers
                - `date /t` → Affiche la date
                """)
            
            if st.button("⚡ Demander l'Exécution", type="primary"):
                if command:
                    # Demande d'autorisation
                    st.markdown("---")
                    if delta.security.request_auth("Exécution Commande", "exec_cmd"):
                        # Exécution
                        result = delta.system.execute_command(command)
                        
                        # Affichage du résultat
                        if result['success']:
                            st.markdown("### ✅ Résultat")
                            if result['output']:
                                st.code(result['output'], language="bash")
                            else:
                                st.info("Commande exécutée sans sortie")
                        else:
                            st.markdown("### ❌ Erreur")
                            st.code(result['error'], language="bash")
                        
                        # Logger l'action
                        delta.memory.log_interaction(
                            "command_executed",
                            command,
                            {"success": result['success'], "return_code": result['return_code']}
                        )
                else:
                    st.warning("⚠️ Veuillez entrer une commande")
        
        # ─────────────────────────────────────────────────────────────────────
        # TAB 2 : Navigation fichiers
        # ─────────────────────────────────────────────────────────────────────
        
        with tab2:
            st.subheader("📁 Navigation dans les Fichiers")
            
            path = st.text_input(
                "Chemin du répertoire",
                value=".",
                help="Chemin du répertoire à explorer (. = répertoire actuel)"
            )
            
            if st.button("📂 Lister les Fichiers", type="primary"):
                files = delta.system.list_directory(path)
                
                if files:
                    st.markdown(f"### 📋 Contenu de `{path}`")
                    st.info(f"{len(files)} élément(s) trouvé(s)")
                    
                    # Affichage en colonnes
                    cols = st.columns(3)
                    for i, file in enumerate(files):
                        with cols[i % 3]:
                            # Icône selon le type
                            if os.path.isdir(os.path.join(path, file)):
                                st.markdown(f"📁 {file}")
                            else:
                                st.markdown(f"📄 {file}")
                else:
                    st.warning("Aucun fichier trouvé ou erreur d'accès")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE 5 : PARAMÈTRES
    # ═══════════════════════════════════════════════════════════════════════════
    
    elif page == "🔧 Paramètres":
        st.header("🔧 Paramètres et Configuration")
        
        # ─────────────────────────────────────────────────────────────────────
        # Sécurité
        # ─────────────────────────────────────────────────────────────────────
        
        st.subheader("🔐 Sécurité")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Code Maître** : Configuré ✅")
            st.caption("Le code maître est défini dans le code source")
        
        with col2:
            st.info(f"**IP Autorisée** : `{AUTHORIZED_IP}`")
            st.caption("Modifiable dans le code source")
        
        st.markdown("---")
        
        # ─────────────────────────────────────────────────────────────────────
        # Base de données
        # ─────────────────────────────────────────────────────────────────────
        
        st.subheader("🗄️ Base de Données")
        
        if delta.db.is_connected():
            st.success("✅ Connexion Supabase active")
            
            # Statistiques
            semantic_count = len(delta.memory.get_semantic())
            episodic_count = len(delta.memory.get_history())
            procedural_count = len(delta.memory.get_habits())
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📚 Faits Sémantiques", semantic_count)
            with col2:
                st.metric("📜 Interactions", episodic_count)
            with col3:
                st.metric("🔄 Habitudes", procedural_count)
        else:
            st.error("❌ Connexion Supabase inactive")
            st.info("Vérifiez que les clés SUPABASE_URL et SUPABASE_KEY sont configurées dans les secrets Streamlit")
        
        st.markdown("---")
        
        # ─────────────────────────────────────────────────────────────────────
        # Informations système
        # ─────────────────────────────────────────────────────────────────────
        
        st.subheader("💻 Informations Système")
        
        sys_info = delta.perception.get_system_info()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Système d'exploitation** : {sys_info['os']}")
            st.info(f"**Architecture** : {sys_info['architecture']}")
        
        with col2:
            st.info(f"**Version Python** : {sys_info['python_version']}")
            st.info(f"**Processeur** : {sys_info['processor']}")
        
        st.markdown("---")
        
        # ─────────────────────────────────────────────────────────────────────
        # Localisation
        # ─────────────────────────────────────────────────────────────────────
        
        st.subheader("📍 Localisation")
        
        loc = delta.perception.get_location()
        st.info(f"**Localisation** : {loc['full']}")
        
        st.markdown("---")
        
        # ─────────────────────────────────────────────────────────────────────
        # À propos
        # ─────────────────────────────────────────────────────────────────────
        
        st.subheader("ℹ️ À Propos")
        
        st.markdown("""
        **DELTA OS** - Digital Enhanced Logical Thinking Assistant  
        Version 1.0  
        
        Créé exclusivement pour **Monsieur Sezer**
        
        **Architecture** :
        - Mémoire Cognitive Quadruple
        - Sécurité Multi-Niveaux
        - Modules : Perception, Communication, Système
        - Base de données : Supabase (PostgreSQL)
        - Interface : Streamlit
        
        **Fonctionnalités** :
        - ✅ Conversation intelligente
        - ✅ Gestion de la mémoire
        - ✅ Communication email
        - ✅ Exécution de commandes système
        - ✅ Navigation fichiers
        
        **Sécurité** :
        - 🔐 Code maître requis pour actions sensibles
        - 🔐 Validation IP
        - 🔐 Logs de toutes les actions
        """)

# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE DE L'APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()

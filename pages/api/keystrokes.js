export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Méthode non autorisée' });
    }

    try {
        const { timestamp, keystrokes } = req.body;
        
        // Pour le moment, on va juste logger les données et renvoyer une réponse
        console.log('Données reçues:', { timestamp, keystrokes });
        
        res.status(200).json({ 
            message: 'Données reçues avec succès',
            data: { timestamp, keystrokes }
        });
    } catch (error) {
        console.error('Erreur:', error);
        res.status(500).json({ message: 'Erreur lors du traitement de la requête' });
    }
} 
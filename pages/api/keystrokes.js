export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Méthode non autorisée' });
    }

    try {
        const { timestamp, keystrokes } = req.body;
        console.log('Données reçues:', { timestamp, keystrokes });
        
        res.status(200).json({ 
            success: true,
            message: 'Données reçues avec succès',
            data: { timestamp, keystrokes }
        });
    } catch (error) {
        console.error('Erreur:', error);
        res.status(500).json({ 
            success: false,
            message: 'Erreur lors du traitement de la requête' 
        });
    }
} 
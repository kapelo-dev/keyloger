import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;

export default async function handler(req, res) {
    // Autoriser CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Gérer les requêtes OPTIONS (pre-flight)
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // Vérifier la méthode
    if (req.method !== 'POST') {
        return res.status(405).json({ 
            error: 'Méthode non autorisée',
            method: req.method,
            allowedMethod: 'POST'
        });
    }

    try {
        // Log pour debug
        console.log('Données reçues:', req.body);

        // Pour le test, on renvoie juste un succès
        return res.status(200).json({ 
            success: true, 
            message: 'Données reçues avec succès',
            data: req.body 
        });

    } catch (error) {
        console.error('Erreur:', error);
        return res.status(500).json({ error: error.message });
    }
} 
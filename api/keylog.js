import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;

export default function handler(req, res) {
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method === 'POST') {
        console.log('Données reçues:', req.body);
        return res.status(200).json({ success: true });
    }

    return res.status(405).json({ error: 'Method not allowed' });
} 
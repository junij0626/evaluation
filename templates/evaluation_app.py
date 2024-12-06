<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluation Results</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        .container {
            max-width: 900px;
            margin: 50px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        .btn {
            display: block;
            width: 150px;
            margin: 0 auto;
            background-color: #007bff;
            color: white;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Evaluation Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Student Name</th>
                    <th>Register Number</th>
                    <th>Marks Obtained</th>
                </tr>
            </thead>
            <tbody>
                {% for result in results %}
                <tr>
                    <td>{{ result.name }}</td>
                    <td>{{ result.register_number }}</td>
                    <td>{{ result.marks }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/logout" class="btn">Logout</a>
    </div>
</body>
</html>

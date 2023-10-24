from ariadne import ObjectType, QueryType, graphql_sync, load_schema_from_path, make_executable_schema
from flask import Flask, request, jsonify
from ariadne.asgi import GraphQL

app = Flask(__name__)
 
schema = load_schema_from_path("schema.graphql")

query = QueryType()
stock = ObjectType("Stock")

@query.field("stock")
def resolve_stocks(*_, ticker):
    stocks = [{
        "name": "Microsoft",
        "ticker": "MSFT",
        "currentPrice": 100.50,
        "historicalPrices": [100.0, 101.0, 99.5, 102.0, 100.5],
        "highestPrice": 102.0,
        "lowestPrice": 99.5,
        "tradingVolume": 100000
    },
    {
        "name": "Alphabet Inc.",
        "ticker": "GOOGL",
        "currentPrice": 2675.00,
        "historicalPrices": [2674.50, 2680.25, 2670.10, 2675.75, 2675.00],
        "highestPrice": 2680.25,
        "lowestPrice": 2670.10,
        "tradingVolume": 800000,
    }]
    for stock in stocks:
        if stock["ticker"] == ticker:
            return stock
        return "Stock not found!"

executable_schema = make_executable_schema(schema, query, stock)


@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(executable_schema, data, context_value={"request": request})
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)

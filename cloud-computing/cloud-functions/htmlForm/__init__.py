import logging

import azure.functions as func


def main(req: func.HttpRequest, inputDocument) -> func.HttpResponse:
    html_data_1 = """
      <title>Message board</title>
      <body>
        <h3>Viktoriia Abakumova</h3>
        <h4> Welcome to the message board. </h4>
        <h4> Messages so far: </h4>
        <ul>
    """
    logging.info('1')
    html_data_message = []

    for doc in inputDocument:
        html_data_message.append(
            "<li>" + str(doc['content']) + "<small> Posted on " + str(doc['message_time']) + "</small></li>")
    html_data_2 = """ {code} """.format(code=(' '.join(html_data_message)))
    logging.info('2')
    html_data_3 = """        
        </ul>

        <h4> Enter a new message</h4>
        <form action="/api/handleMessage">
            <label> Your message: </label><br>
            <input type="text" name="msg"><br>
            <input type="submit" value="Submit">
        </form>
        </body>
        </html>
    """

    logging.info('Python HTTP trigger function processed a request.')
    a = html_data_1 + html_data_2 + html_data_3
    return func.HttpResponse(
        a,
        status_code=200,
        mimetype="text/html"
    )


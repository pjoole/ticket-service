from flask import Blueprint, request, jsonify, abort
from PIL import Image
import numpy as np
from ticket_service.data import Ticket

import qrcode
import base64
import io
import cv2

ticket_service = Blueprint('ticket_service', __name__)

# Let's keep it simple and store all tickets in memory
tickets = {}

@ticket_service.route('<string:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = tickets.get(ticket_id)

    if ticket is None:
        abort(400)

    return jsonify(ticket), 200

@ticket_service.route('', methods=['POST'])
def create_ticket():
    if not request.json:
        abort(400)
    if 'event_name' not in request.json:
        abort(400)
    if 'event_timestamp' not in request.json:
        abort(400)
    if 'event_place' not in request.json:
        abort(400)

    ticket = Ticket(request.json['event_name'],
                    request.json['event_timestamp'],
                    request.json['event_place'],
                    request.json['seat'],
                    request.json['owner'])

    qr = qrcode.QRCode()
    qr.add_data('http://localhost:5000/api/tickets/' + ticket.id)
    image = qr.make_image()
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format="JPEG")
    encodedImg = base64.b64encode(in_mem_file.getvalue())

    tickets.update({ticket.id: ticket})

    return jsonify({'id': ticket.id,
                    'qr_code': encodedImg.decode('ascii')}), 201

@ticket_service.route('validate', methods=['PUT'])
def validate_ticket():
    if not request.json:
        abort(400)
    if 'qr_code' not in request.json:
        abort(400)
    decodedImg = base64.b64decode(request.json['qr_code'])
    image = Image.open(io.BytesIO(decodedImg))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    d = cv2.QRCodeDetector()
    val, _, _ = d.detectAndDecode(img)

    return val
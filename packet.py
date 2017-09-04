class Packet(object):
    def __init__(self, magic_no, p_type, seq_no, data_len, data):
        # Magic number
        self.magic_no = magic_no

        # Packet type must be of dataPacket or acknowledgementPacket
        data_packet = 0
        acknowledgement_packet = 1
        if p_type != data_packet or p_type != acknowledgement_packet:
            raise Exception("Incorrect packet type")
        self.p_type = p_type

        # Sequence value in binary
        if not all(c in '01' for c in seq_no):
            raise Exception("Packet non-binary sequence number")
        self.seq_no = seq_no

        # Data length field, 0 <= x <= 512
        if data_len < 0 or data_len > 512:
            raise Exception("Invalid packet data length")
        self.data_len = data_len

        # Actual packet payload
        self.data = data

    def get_magic_no(self):
        return self.magic_no

    def get_packet_type(self):
        # Flag for if connecting packet or final packet (I think??)
        return self.p_type

    def get_packet_sequence_no(self):
        return self.seq_no

    def get_data_len(self):
        return self.data_len

    def get_packet_payload(self):
        return self.data

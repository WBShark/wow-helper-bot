# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: log_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11log_service.proto\x12\rwowlogfetcher\"+\n\tDRRequest\x12\x0c\n\x04\x64ung\x18\x01 \x01(\t\x12\x10\n\x08rio_link\x18\x02 \x01(\t\"I\n\tRRRequest\x12\x0c\n\x04raid\x18\x01 \x01(\t\x12\x12\n\x05\x64\x66\x66\x66\x63\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x10\n\x08rio_link\x18\x03 \x01(\tB\x08\n\x06_dfffc\" \n\x0c\x42ossResponse\x12\x10\n\x08rankings\x18\x01 \x03(\x05\",\n\nDRResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08rankings\x18\x02 \x03(\x05\"\xa3\x01\n\nRRResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x39\n\x08rankings\x18\x02 \x03(\x0b\x32\'.wowlogfetcher.RRResponse.RankingsEntry\x1aL\n\rRankingsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.wowlogfetcher.BossResponse:\x02\x38\x01\x32\x9d\x01\n\nLogFetcher\x12H\n\x0fGetDungeonRanks\x12\x18.wowlogfetcher.DRRequest\x1a\x19.wowlogfetcher.DRResponse\"\x00\x12\x45\n\x0cGetRaidRanks\x12\x18.wowlogfetcher.RRRequest\x1a\x19.wowlogfetcher.RRResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'log_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RRRESPONSE_RANKINGSENTRY._options = None
  _RRRESPONSE_RANKINGSENTRY._serialized_options = b'8\001'
  _DRREQUEST._serialized_start=36
  _DRREQUEST._serialized_end=79
  _RRREQUEST._serialized_start=81
  _RRREQUEST._serialized_end=154
  _BOSSRESPONSE._serialized_start=156
  _BOSSRESPONSE._serialized_end=188
  _DRRESPONSE._serialized_start=190
  _DRRESPONSE._serialized_end=234
  _RRRESPONSE._serialized_start=237
  _RRRESPONSE._serialized_end=400
  _RRRESPONSE_RANKINGSENTRY._serialized_start=324
  _RRRESPONSE_RANKINGSENTRY._serialized_end=400
  _LOGFETCHER._serialized_start=403
  _LOGFETCHER._serialized_end=560
# @@protoc_insertion_point(module_scope)

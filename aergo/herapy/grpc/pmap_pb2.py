# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pmap.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import node_pb2 as node__pb2
from . import p2p_pb2 as p2p__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pmap.proto',
  package='types',
  syntax='proto3',
  serialized_options=_b('Z\036github.com/aergoio/aergo/types'),
  serialized_pb=_b('\n\npmap.proto\x12\x05types\x1a\nnode.proto\x1a\tp2p.proto\"X\n\x08MapQuery\x12\x1d\n\x06status\x18\x01 \x01(\x0b\x32\r.types.Status\x12\r\n\x05\x61\x64\x64Me\x18\x02 \x01(\x08\x12\x0c\n\x04size\x18\x03 \x01(\x05\x12\x10\n\x08\x65xcludes\x18\x04 \x03(\x0c\"j\n\x0bMapResponse\x12#\n\x06status\x18\x01 \x01(\x0e\x32\x13.types.ResultStatus\x12%\n\taddresses\x18\x02 \x03(\x0b\x32\x12.types.PeerAddress\x12\x0f\n\x07message\x18\x03 \x01(\tB Z\x1egithub.com/aergoio/aergo/typesb\x06proto3')
  ,
  dependencies=[node__pb2.DESCRIPTOR,p2p__pb2.DESCRIPTOR,])




_MAPQUERY = _descriptor.Descriptor(
  name='MapQuery',
  full_name='types.MapQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='types.MapQuery.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='addMe', full_name='types.MapQuery.addMe', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size', full_name='types.MapQuery.size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='excludes', full_name='types.MapQuery.excludes', index=3,
      number=4, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=132,
)


_MAPRESPONSE = _descriptor.Descriptor(
  name='MapResponse',
  full_name='types.MapResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='types.MapResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='addresses', full_name='types.MapResponse.addresses', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='types.MapResponse.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=240,
)

_MAPQUERY.fields_by_name['status'].message_type = p2p__pb2._STATUS
_MAPRESPONSE.fields_by_name['status'].enum_type = p2p__pb2._RESULTSTATUS
_MAPRESPONSE.fields_by_name['addresses'].message_type = node__pb2._PEERADDRESS
DESCRIPTOR.message_types_by_name['MapQuery'] = _MAPQUERY
DESCRIPTOR.message_types_by_name['MapResponse'] = _MAPRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MapQuery = _reflection.GeneratedProtocolMessageType('MapQuery', (_message.Message,), dict(
  DESCRIPTOR = _MAPQUERY,
  __module__ = 'pmap_pb2'
  # @@protoc_insertion_point(class_scope:types.MapQuery)
  ))
_sym_db.RegisterMessage(MapQuery)

MapResponse = _reflection.GeneratedProtocolMessageType('MapResponse', (_message.Message,), dict(
  DESCRIPTOR = _MAPRESPONSE,
  __module__ = 'pmap_pb2'
  # @@protoc_insertion_point(class_scope:types.MapResponse)
  ))
_sym_db.RegisterMessage(MapResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

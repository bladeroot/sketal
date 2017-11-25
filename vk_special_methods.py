# -*- coding: utf-8 -*-
from typing import Optional, BinaryIO

import aiohttp
import json

from vk_plus_utils import Attachment


async def upload_audio_message(api, multipart_data, peer_id) -> Optional[Attachment]:
    """Upload audio file `multipart_data` and return Attachment for sending to user with id `peer_id`(possibly)"""

    sender = api.get_default_sender("docs.getMessagesUploadServer")
    client = api.get_current_sender("docs.getMessagesUploadServer", sender=sender)

    data = aiohttp.FormData()
    data.add_field('file', multipart_data, filename="message.mp3", content_type='multipart/form-data')

    values = {'type': "audio_message", 'peer_id': peer_id}

    if client.group_id:
        values['group_id'] = client.group_id

    response = await api(sender=sender).docs.getMessagesUploadServer(**values)

    if not response or not response.get('upload_url'):
        return None

    upload_url = response['upload_url']

    async with aiohttp.ClientSession() as sess:
        async with sess.post(upload_url, data=data) as resp:
            result = json.loads(await resp.text())

    if not result:
        return None

    data = dict(file=result['file'])
    result = (await api(sender=sender).docs.save(**data))[0]

    return Attachment.from_upload_result(result, "doc")


async def upload_doc(api, multipart_data, filename="image.png") -> Optional[Attachment]:
    """Upload file `multipart_data` and return Attachment for sending to user"""

    sender = api.get_default_sender("docs.getWallUploadServer")
    client = api.get_current_sender("docs.getWallUploadServer", sender=sender)

    data = aiohttp.FormData()
    data.add_field('file', multipart_data, filename=filename, content_type='multipart/form-data')

    values = {}

    if client.group_id:
        values['group_id'] = client.group_id

    response = await api(sender=sender).docs.getWallUploadServer(**values)

    if not response or not response.get('upload_url'):
        return None

    upload_url = response['upload_url']

    async with aiohttp.ClientSession() as sess:
        async with sess.post(upload_url, data=data) as resp:
            result = json.loads(await resp.text())

    if not result:
        return None

    data = dict(file=result['file'])
    result = (await api(sender=sender).docs.save(**data))[0]

    return Attachment.from_upload_result(result, "doc")


async def upload_photo(api, multipart_data, peer_id=None):
    """ Upload photo file `multipart_data` and return Attachment for sending to
    user with id `peer_id`(optional but recommended)
    """

    sender = api.get_default_sender('photos.getMessagesUploadServer')

    data = aiohttp.FormData()
    data.add_field('photo', multipart_data, filename='picture.png', content_type='multipart/form-data')

    kwargs = {}
    if peer_id:
        kwargs["peer_id"] = peer_id

    response = await api(sender=sender).photos.getMessagesUploadServer(**kwargs)

    if not response or not response.get('upload_url'):
        return None

    upload_url = response['upload_url']

    async with aiohttp.ClientSession() as sess:
        async with sess.post(upload_url, data=data) as resp:
            result = json.loads(await resp.text())

    if not result:
        return None

    data = {'photo': result['photo'], 'hash': result['hash'], 'server': result['server']}
    result = await api(sender=sender).photos.saveMessagesPhoto(**data)

    if not result:
        return None

    return Attachment.from_upload_result(result[0])

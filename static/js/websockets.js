"use strict";
let ws = null;
let sendButton = null;
let users = [];
let tips = null;
let search = null;

window.addEventListener('load', () => {
    ws = new WebSocket(('ws://localhost:8181/'));
    sendButton = document.querySelector('#send-button');
    search = document.querySelector('#user-search');
    tips = document.querySelector('#tips');
    sendButton.addEventListener('click', async event => sendMessage(event));
    tips.addEventListener('click', event => searchUsers(event));
    const notif = document.querySelector('.notification');
    notif.addEventListener('dblclick', event => {
       event.target.classList.remove('show');
    });
    ws.addEventListener('open', () => {
        const userId = document.querySelector('#user-id').value;
        const data = {
            'kind': 'init',
            'from_user': userId
        }
        ws.send(JSON.stringify(
            data
        ));
    });
    ws.addEventListener('message', message => newMessageFunction(message));
});

window.addEventListener('load', async () => {
    const messagesLink = document.querySelector('#messages-link');
    messagesLink.addEventListener('click', (event) => showDialog(event));
    const messengerContacts = document.querySelector('.contacts-list');
    messengerContacts.addEventListener('click', async (event) => await showMessages(event));
    const closeButton = document.querySelector('.close-button');
    closeButton.addEventListener('click', () => {
        const frame = document.querySelector('.messages-form-container');
        frame.classList.remove('display-flex');
    })
    search.addEventListener('click', async () => {
        const request = new Request(
        'http://localhost:8000/users_list/'
        );
        users = await fetch(request
        ).then(
            result => result.json()
        ).catch(
            err => console.log(err)
        );
    });
    search.addEventListener('input', event => showTips(event.target));
});

window.addEventListener('click', event => {
    const search = document.querySelector('#user-search');
    if (event.target !== tips && event.target !== search) {
        tips.style.display = 'none';
    }
})

function addMessage(chat, item) {
    let chatItem = document.createElement('li');
    chatItem.className = 'chat-item';
    chatItem.innerHTML = item;
    chat.append(chatItem);
}

function showDialog(event) {
    event.target.innerText = 'Сообщения';
    const container = document.querySelector('.messages-form-container');
    container.classList.add('display-flex');
}


function newNotification(data) {
    const container = document.querySelector('.messages-list');
    const newNotify = document.createElement('LI');
    let ts = data.timestamp.split('T').join(' ').split('.')[0];
    newNotify.className = 'message-item';
    if (data.kind === 'notify') {
        newNotify.innerHTML = `<label>${ts}</label><br>${data.text}`;
    } else {
        newNotify.innerHTML = `<b>У вас новое сообщение</b>`;
    }
    container.appendChild(newNotify);
    const bubbling = document.querySelector('.notification');
    bubbling.innerHTML = newNotify.innerHTML;
    bubbling.classList.add('show');
}

function newMessage(data) {
    const chatBox = document.querySelector('.chat-box');
    if (chatBox.parentElement.parentElement.classList.contains('display-flex')) {
        if (chatBox.querySelector('#text').dataset.id === data.from_user) {
            addMessage(chatBox.querySelector('.chat'), `<b>${data.timestamp}</b><br>${data.text}`);
        } else {
            const contacts = document.querySelectorAll('.contacts-item');
            contacts.forEach(el => {
                if (el.dataset.id === data.from_user) {
                    el.innerHTML = `${el.innerText}<br><b>NEW</b>`
                }
            })
        }
    } else {
        document.querySelector('#messages-link').innerText += ' (1)';
    }
}

function newMessageFunction(message) {
    const data = JSON.parse(message.data);
    if (data.kind === 'notify') {
        newNotification(data);
    } else {
        newNotification(data);
        newMessage(data);
    }

}

async function sendMessage(event) {
    const fromUser = document.querySelector('#user-id').value;
    const toUser = event.target.previousElementSibling.dataset.id;
    const input = event.target.previousElementSibling;
    const text = input.value;
    input.value = '';
    await ws.send(
        JSON.stringify({
            'kind': 'message',
            'from_user': fromUser,
            'to_user': toUser,
            'text': text
        })
    );
    let today = new Date();
    const hours = today.getHours();
    const minutes = today.getMinutes();
    addMessage(
        document.querySelector('.chat'),
        `<b>${hours}:${minutes}</b><br>${text}`
    );
}

async function showMessages(event) {
    if (event.target.className === 'contacts-item') {
        event.target.querySelectorAll('B').forEach(el => el.remove());
        event.target.querySelectorAll('BR').forEach(el => el.remove());
        document.querySelectorAll('.contacts-item').forEach(el => {
            if (el.classList.contains('background-color')) {
                el.classList.remove('background-color')
            }
        });
        event.target.classList.add('background-color');
        const request = new Request(
            `http://localhost:8000/messages_list/${event.target.dataset.id}/`
        )
        const response = await fetch(request).then(
            result => result.json()
        ).catch(
            err => console.log(err)
        );
        const chat = document.querySelector('.chat');
        const sendForm = document.querySelector('#send-form');
        const inputEl = sendForm.querySelector('#text');
        inputEl.dataset.id = event.target.dataset.id;
        sendForm.style.display = 'flex';
        chat.querySelectorAll('LI').forEach(el => el.remove());
        for (let item of response.result) {
            addMessage(chat, item);
        }
    }
}

function searchUsers(event) {
    if (event.target.tagName === 'LI') {
        const contacts = document.querySelector('.contacts-list');
        event.target.className = 'contacts-item';
        for (let child of contacts.children) {
            if (child.dataset.id === event.target.dataset.id) {
                child.remove();
            }
        }
        search.querySelector('INPUT').value = '';
        tips.style.display = 'none';
        contacts.appendChild(event.target);
        showMessages(event);
    }
}

function showTips(target) {
    const old = tips.querySelector('ul');
    if (old) {
        old.remove();
    }
    tips.style.display = 'block';
    const html = document.createElement('ul');
    for (let i of users.result) {
        if (i.name.includes(target.value)) {
            const li = document.createElement('li');
            li.dataset.id = i.id;
            li.innerText = i.name;
            html.append(li);
        }
    }
    tips.appendChild(html);
}

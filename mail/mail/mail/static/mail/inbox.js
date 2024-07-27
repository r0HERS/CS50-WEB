document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-all').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = function (event) {
    event.preventDefault();
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      })
    })
    .then(response => {
      if (response.status === 201) {
        return response.json();
      } else {
        throw new Error('Failed to send email');
      }
    })
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-all').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  let isInbox = (mailbox === 'inbox');
  let isArchive = (mailbox === 'archive');
  let isSent = (mailbox === 'sent');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => add_email(email, isInbox, isArchive, isSent));
  });
}

function add_email(emailData, isInbox, isArchive, isSent) {
  const email = document.createElement('div');
  email.className = 'email';

  let backgroundColorClass = emailData.read ? 'email-read' : 'email-unread';

  let archiveButton;
  if (isInbox) {
    archiveButton = `<button id="archiveButton-${emailData.id}" class="btn btn-lg btn-primary align-self-center">Archive</button>`;
  } else if (isArchive) {
    archiveButton = `<button id="archiveButton-${emailData.id}" class="btn btn-lg btn-primary align-self-center">Unarchive</button>`;
  } else {
    archiveButton = "";
  }

  email.innerHTML = `
    <div class="card-body ${backgroundColorClass} border-dark">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h5 class="card-title">${emailData.sender}</h5>
          <h6 class="card-subtitle mb-2 text-muted">${emailData.subject}</h6>
          <p class="card-text">${emailData.timestamp}</p>
        </div>
        <div>
          ${archiveButton}
        </div>
      </div>
    </div>
  `;

  document.querySelector('#emails-view').append(email);

  if (isInbox || isArchive) {
    const archiveButtonElement = document.getElementById(`archiveButton-${emailData.id}`);
    if (archiveButtonElement) {
      archiveButtonElement.addEventListener('click', (event) => {
        event.stopPropagation();
        archive_email(emailData);
      });
    }
  }

  email.addEventListener('click', function() {
    view_email(emailData, isInbox, isArchive, isSent);
  });
}

function view_email(emailData, isInbox, isArchive, isSent) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-all').style.display = 'block';

  let replyButton = !isSent ? `<button id="replyButton" class="btn btn-primary mb-3">Reply</button>` : "";

  let archiveButton;
  if (isInbox) {
    archiveButton = `<button id="archiveButton" class="btn btn-primary mb-3">Archive</button>`;
  } else if (isArchive) {
    archiveButton = `<button id="archiveButton" class="btn btn-primary mb-3">Unarchive</button>`;
  } else {
    archiveButton = "";
  }

  document.querySelector('#email-all').innerHTML = `
    <div>
      <div class="card-body">
        <h5 class="card-title">From: ${emailData.sender}</h5>
        <h6 class="card-subtitle mb-2 text-muted">To: ${emailData.recipients.join(', ')}</h6>
        <h6 class="card-subtitle mb-2 text-muted">Subject: ${emailData.subject}</h6>
        <h6 class="card-subtitle mb-2 text-muted">Timestamp: ${emailData.timestamp}</h6>
        <hr>
        ${replyButton} ${archiveButton}
        <p class="card-text">${emailData.body}</p>
      </div>
    </div>
  `;

  fetch(`/emails/${emailData.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });

  if (!isSent) {
    const replyButtonElement = document.querySelector('#replyButton');
    replyButtonElement.addEventListener('click', function() {
      compose_email();
  
      document.querySelector('#title').innerHTML = 'New Email Response';
      document.querySelector('#compose-recipients').value = emailData.sender;
    
      let subject = emailData.subject;
    
      if (!/^Re:/.test(subject)) {
        subject = "Re: " + subject;
      }
    
      document.querySelector('#compose-subject').value = subject;
    
      document.querySelector('#compose-body').value = `On ${emailData.timestamp} ${emailData.sender} wrote: ${emailData.body}`;
    });
  }

  if (archiveButton) {
    const archiveButtonElement = document.querySelector("#archiveButton");
    archiveButtonElement.addEventListener('click', () => {
      archive_email(emailData);
    });
  }
}

function archive_email(emailData) {
  fetch(`/emails/${emailData.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !emailData.archived
    })
  })
  .then(() => {
    load_mailbox('inbox');
  });
}

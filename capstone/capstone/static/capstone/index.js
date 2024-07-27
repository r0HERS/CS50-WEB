document.addEventListener('DOMContentLoaded', function () {
    const inviteBtn = document.getElementById('invite_icon');
    const invitesList = document.getElementById('invites_list');

    inviteBtn.addEventListener('click', function listHandler(event) {
        event.preventDefault();
        
        if (invitesList.style.display === 'block') {
            invitesList.style.display = 'none';
        } else {
            invitesList.style.display = 'block';
        }

    });

    document.querySelectorAll('.accept').forEach(acceptBtn => {
        acceptBtn.addEventListener('click', function(){
            const invite_id = this.getAttribute('data-invite_id');
            const li = document.getElementById(`invite-${invite_id}`);
            console.log(invite_id);

            fetch(`/accept_invite/${invite_id}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    li.remove();
                    const badge = document.getElementById('badge_count');
                    let count = parseInt(badge.textContent);
                    count = count -1;
                    badge.textContent = count;
                    showAlert('Invite accepted successfully', 'success');
                    console.log('Invite accepted successfully');
                    location.reload();
                } else {
                    showAlert('Failed to decline invite', 'danger');
                    console.error('Failed to accept invite');
                }
            });

        })
    })

    document.querySelectorAll('.decline').forEach(declineBtn => {
        declineBtn.addEventListener('click', function(){
            const invite_id = this.getAttribute('data-invite_id');
            const li = document.getElementById(`invite-${invite_id}`);
            console.log(invite_id)

            fetch(`/decline_invite/${invite_id}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    li.remove();
                    const badge = document.getElementById('badge_count');
                    let count = parseInt(badge.textContent);
                    count = count -1;
                    badge.textContent = count;
                    showAlert('Invite declined successfully', 'danger');
                    console.log('Invite accepted successfully');
                } else {
                    showAlert('Failed to decline invite', 'danger');
                    console.error('Failed to accept invite');
                }
            });

        })
    })

    const inviteFormBtn = document.getElementById('invite-btn');
    const inviteForm = document.getElementById('invite_form');
    const sendInviteBtn = document.getElementById('sendinvite-btn');

    if(inviteFormBtn){
       inviteFormBtn.addEventListener('click', function () {
            inviteForm.style.display = 'block';
            inviteFormBtn.style.display = 'none';
        }); 
    }
        
    if(sendInviteBtn){
        sendInviteBtn.addEventListener('click', function () {
            inviteForm.style.display = 'none';
            inviteFormBtn.style.display = 'block';

            const project_id = document.getElementById('projectId').value;
            const selectedUser_id = document.getElementById('userSelect').value;

            fetch(`/invite/${selectedUser_id}`, {
                method: 'POST',
                body: JSON.stringify({
                    project_id: project_id,
                }),
            })
            .then(response => {
                if (response.ok) {
                    showAlert('Invite sent successfully', 'success');
                    console.log('Invite sent successfully');
                } else {
                    showAlert('Failed to send invite', 'danger');
                    console.error('Failed to send invite');
                }
            });
        });
    }
        

    var calendarEl = document.getElementById('calendar');
    const project_id = calendarEl.getAttribute('data-project_id');
    var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          events: `/get_events/${project_id}`,  
          eventClick: function(info) {
            var taskId = info.event.id;
            var taskElement = document.getElementById(`task-${taskId}`);
            if (taskElement) {
                taskElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }

        });
        calendar.render();


    document.querySelectorAll('.complete-task').forEach(completeBtn => {
        completeBtn.addEventListener('click', function(){

            const task_id = this.getAttribute('data-task_id');
            console.log(task_id)

            fetch(`/complete_task/${task_id}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    showAlert('Task completed successfully', 'success');
                    console.log('Task completed successfully');
                    const taskItem = document.getElementById(`task-${task_id}`);
                    taskItem.classList.add('complete-task-container');
                    const addcomment = document.getElementById(`add-comment-${task_id}`);
                    addcomment.style.display = 'none';
                    const completeBtnContainer = taskItem.querySelector('.complete-task');
                    taskItem.classList.remove('task-ontime', 'task-overdue');
                    if (completeBtnContainer) {
                        completeBtnContainer.innerHTML = '<p class="btn btn-dark btn-sm">Completed</p>';
                    }
                    updateProgressBar();
                } else {
                    showAlert('Failed to complete task', 'danger');
                    console.error('Failed to complete task');
                }
            });

        })
    })

    document.querySelectorAll('.delete-task').forEach(completeBtn => {
        completeBtn.addEventListener('click', function(){

            const task_id = this.getAttribute('data-task_id');
            console.log(task_id)

            fetch(`/delete_task/${task_id}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    showAlert('Task deleted successfully', 'danger');
                    console.log('Task deleted successfully');
                    const taskItem = document.getElementById(`task-${task_id}`);
                    taskItem.remove()
                    updateProgressBar();
                } else {
                    showAlert('Failed to delete task', 'danger');
                    console.error('Failed to delete task');
                }
            });

        })
    })


    document.querySelectorAll('.delete-btn').forEach(deleteBtn => {
        deleteBtn.addEventListener('click', function(){
            const project_id = this.getAttribute('data-project_id');
            console.log(project_id)
            const project_card = document.getElementById(`card-${project_id}`)

            fetch(`/delete_project/${project_id}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    showAlert('Project deleted successfully', 'success');
                    console.log('Project deleted successfully');
                    project_card.remove()
                } else {
                    showAlert('Failed to delete project', 'danger');
                    console.error('Failed to delete project');
                }
            });
        
        })
    })

    document.querySelectorAll('.edit-task').forEach(edit_task => {
        edit_task.addEventListener('click', function editHandler(){
            const task_id = this.getAttribute('data-task_id');
            console.log(task_id);
            
            const task_info = document.getElementById(`task-info-${task_id}`);
            const edit_task = document.getElementById(`edit-${task_id}`);

            task_info.style.display = 'none';
            edit_task.style.display = 'block';



            const edit_title = document.getElementById(`taskTitle-${task_id}`);
            const edit_description = document.getElementById(`taskDescription-${task_id}`);
            const edit_time = document.getElementById(`taskTime-${task_id}`);
            const edit_start = document.getElementById(`start_date-${task_id}`);
            const edit_due = document.getElementById(`due_date-${task_id}`);

            
            this.innerHTML = '<button class="btn btn-primary btn-sm">Save</button>'

            this.removeEventListener('click', editHandler);
            this.addEventListener('click', function saveHandler(){

                task_info.style.display = 'block';
                edit_task.style.display = 'none';

                fetch(`/edit_task/${task_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        title: edit_title.value,
                        description: edit_title.value,
                        time: edit_time.value,
                        start_date: edit_start.value,
                        due_date: edit_due.value,
                    })
                  })

                  .then(data => { 
                    document.getElementById(`infoTitle-${task_id}`).innerText = edit_title.value;
                    document.getElementById(`infoDescription-${task_id}`).innerText = edit_title.value;
                    document.getElementById(`info_start-${task_id}`).innerText = edit_start.value;
                    document.getElementById(`info_due-${task_id}`).innerText = edit_due.value;
                    document.getElementById(`infoTime-${task_id}`).innerText = `Estimated Time: ${edit_time.value} Hours`;

                    this.removeEventListener('click', saveHandler);
                    this.addEventListener('click', editHandler)
                    this.innerHTML = '<button class="btn btn-primary btn-sm">Edit</button>'
                })
                
            })
        
        })
    })


    function updateProgressBar() {
        const totalTasks = document.querySelectorAll('.list-group-item').length;
        const completedTasks = document.querySelectorAll('.complete-task-container').length;
        const completionPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
    
        const progressBar = document.getElementById('progress-bar');
        progressBar.style.width = `${completionPercentage}%`;
        progressBar.innerText = `${Math.round(completionPercentage)}%`;
        progressBar.setAttribute('aria-valuenow', Math.round(completionPercentage));
    }
    

    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        alertContainer.appendChild(alert);
    
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
    
});

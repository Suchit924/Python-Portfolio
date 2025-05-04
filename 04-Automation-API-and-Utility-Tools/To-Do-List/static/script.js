const tasks = document.querySelectorAll('.task');
const columns = document.querySelectorAll('.column');

tasks.forEach(task => {
    task.addEventListener('dragstart', () => {
        task.classList.add('dragging');
    });

    task.addEventListener('dragend', () => {
        task.classList.remove('dragging');
    });
});

columns.forEach(column => {
    column.addEventListener('dragover', e => {
        e.preventDefault();
        const draggingTask = document.querySelector('.dragging');
        column.appendChild(draggingTask);

        const newStatus = column.id;
        const taskId = draggingTask.getAttribute('data-id');

        // Update the server
        fetch(`/move/${taskId}/${newStatus}`);
    });
});

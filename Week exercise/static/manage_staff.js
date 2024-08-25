function addStaff(id, csrf_token){
    const staff_id = document.getElementById('input-add-staff').value;
    // กำหนด path ให้ถูกต้อง
    fetch(`/employee/project/detail/${id}/add/${staff_id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
    })
    .then(data => {
        console.log('Item updated successfully')
        window.location.reload()
    })
    .catch(error => console.error('Error:', error));
}


async function removeStaff(pro_id, emp_id, csrf_token){
    // กำหนด path ให้ถูกต้อง
    fetch(`/employee/project/detail/${pro_id}/remove/${emp_id}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
    })
    .then(data => {
        console.log('Item updated successfully')
        window.location.reload()
    })
    .catch(error => console.error('Error:', error));
}
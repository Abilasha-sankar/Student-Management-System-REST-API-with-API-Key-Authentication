const API_KEY = "STUDENT123";
const BASE_URL = "http://localhost:8081/student";
// CREATE
function createStudent() {
    let id = document.getElementById("id").value;
    let name = document.getElementById("name").value;
    if (id === "" || name === "") {
        alert("Please enter Student ID and Student Name");
        return;
    }
    fetch(BASE_URL + "?id=" + id + "&name=" + encodeURIComponent(name), {
        method: "POST",
        headers: {
            "X-API-KEY": API_KEY
        }
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("output").textContent = data;
        clearFields();
    });
}
// DISPLAY
function displayStudents() {
    fetch(BASE_URL, {
        method: "GET",
        headers: {
            "X-API-KEY": API_KEY
        }
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("output").textContent = data;
    });
}
// UPDATE
function updateStudent() {
    let id = document.getElementById("id").value;
    let name = document.getElementById("name").value;
    if (id === "" || name === "") {
        alert("Please enter Student ID and New Name");
        return;
    }
    fetch(BASE_URL + "?id=" + id + "&name=" + encodeURIComponent(name), {
        method: "PUT",
        headers: {
            "X-API-KEY": API_KEY
        }
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("output").textContent = data;
        clearFields();
    });
}
// DELETE
function deleteStudent() {
    let id = document.getElementById("id").value;
    if (id === "") {
        alert("Please enter Student ID");
        return;
    }
    fetch(BASE_URL + "?id=" + id, {
        method: "DELETE",
        headers: {
            "X-API-KEY": API_KEY
        }
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("output").textContent = data;
        clearFields();
    });
}
// CLEAR
function clearFields() {
    document.getElementById("id").value = "";
    document.getElementById("name").value = "";
}
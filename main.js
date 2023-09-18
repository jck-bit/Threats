const fetchUsers = async () =>{
    const res = await fetch('http://127.0.0.1:8000/suggested-users/');
    const data = await res.json();
    console.log(data);
    return data;

}


fetchUsers()
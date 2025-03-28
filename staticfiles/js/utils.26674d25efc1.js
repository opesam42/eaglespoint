function getCsrfToken() {
    let csrfToken = null;
    document.cookie.split(";").forEach(cookie => {
        const [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
            csrfToken = value;
        }
    });
    return csrfToken;
}

async function handleLogin(event){
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const jsonData  = JSON.stringify(Object.fromEntries(formData));

    try{
        const response = await fetch("/user/login/", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: jsonData,
        });

        const result = await response.json();

        const errorMessageContainer = form.querySelector('#error-message')
        console.log(errorMessageContainer)

        if(!response.ok){
            errorMessageContainer.textContent = result.message;
            errorMessageContainer.classList.remove("hidden");
            return;
        } 
        
        // if successful
        errorMessageContainer.classList.add("hidden");
        console.log(result.message);

    } catch(error){
        console.error("Error:", error);
    }
}

async function fetchLGAs(state){
    try{
        const response = await fetch( "/listing/get-states/" );
        if(!response.ok) throw new Error("Failed to fetch LGAs");

        const data = await response.json();
        lgas = data[state];
        return lgas;
        
    } catch(error){
        console.error('Error:', error);
        return [];
    }
}
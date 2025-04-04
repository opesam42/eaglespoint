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


async function handlePasswordReset(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const messageBox = form.querySelector('#message')
    messageBox.innerHTML = "";
    // messageBox.classList.innerHTML = "";

    try{
        const response = await fetch('/user/password-reset/', {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                // "Content-Type": "application/json", // i am not sending json data
                "X-CSRFToken": getCsrfToken(),
            },
            body: formData,
        });

        const result = await response.json();

        if(!response.ok){
            console.log(result.message);
            messageBox.classList.remove('hidden');
            messageBox.classList.add('text-red-800', 'bg-red-100');
            messageBox.innerHTML = result.message;
            return;
        } 

        // if successful
        messageBox.classList.remove('hidden')
        messageBox.classList.add('text-green-800', 'bg-green-100');
        messageBox.innerHTML = result.message;
        console.log(result.message);
        return;

    } catch (error) {
        messageBox.classList.remove('hidden');
        messageBox.classList.add('text-red-800', 'bg-red-100');
        messageBox.innerHTML = "An unexpected error occurred. Please try again.";
        console.error('Error:', error);
    }

}

async function handleSignUp(event){
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const jsonData  = JSON.stringify(Object.fromEntries(formData));

    // loading effect on frontend
    const submitBtn = form.querySelector('button[type="submit"]');
    originalText = submitBtn.innerHTML   
    submitBtn.disabled = true; //prevent double click 
    submitBtn.innerHTML = `<i class="fa fa-spinner fa-spin"></i> Creating account...`;

    try{
        const response = await fetch("/user/register/", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: jsonData,
        });

        const result = await response.json();

        if(!response.ok){
            displayFormError(result.errors, form);
            console.log(result.errors);
            return;
        } 
        
        const notification_div = form.querySelector("#notification");
        notification_div.classList.remove("hidden");
        notification_div.classList.add("bg-green-100", "text-green-500");
        notification_div.innerText = result.message;
        console.log(result.message);

    } catch(error){
        console.error("Error:", error);
    } finally{
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }

}


function displayFormError(errors, form){
    form.querySelectorAll('.error-message').forEach(error => error.remove());

    Object.keys(errors).forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        
        if(field){
            const errorDiv = document.createElement('div');
            errorDiv.className = "error-message text-red-500 text-sm";
            errorDiv.innerText = errors[fieldName].join(",");
            field.after(errorDiv);
        }
    });

}

async function handleLogin(event){
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const jsonData  = JSON.stringify(Object.fromEntries(formData));

    // loading effect on frontend
    const submitBtn = form.querySelector('button[type="submit"]');
    originalText = submitBtn.innerHTML   
    submitBtn.disabled = true; //prevent double click 
    submitBtn.innerHTML = `<i class="fa fa-spinner fa-spin"></i> Login in...`;

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
            console.log(result.message)
            if(result.message == "Verification email sent"){
                errorMessageContainer.innerHTML = "Your account has not been verified. A verification mail has been sent to your email";
                errorMessageContainer.classList.remove("hidden");
                return;
            }
            if(result.message == "Invalid login details"){
                errorMessageContainer.innerHTML = "Invalid login details. Check your email and password";
            }

            errorMessageContainer.innerHTML = result.message;
            errorMessageContainer.classList.remove("hidden");
            return;
        } 
        
        // if successful
        errorMessageContainer.classList.add("hidden");
        window.location.href = result.next_url
        console.log(result.message);
        console.log(result.next_url);

    } catch(error){
        console.error("Error:", error);
    } finally{
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
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
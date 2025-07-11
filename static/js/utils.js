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

// for forget password
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
    form.querySelectorAll('.error-message').forEach(error => error.remove());
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
        console.log(result)
        if(result.status == 'error'){
            errorMessageContainer.classList.add("hidden");
            switch(result.error_type){
                case 'user_not_verified':
                    errorMessageContainer.innerHTML = "Your account has not been verified. A verification mail has been sent to your email";
                    break;
                case 'invalid_credentials':
                    message = "Invalid login details. Check your email and password"
                    // showToastNotification('danger', message);
                    errorMessageContainer.innerHTML = message;
                    break;
                case 'blocked_user':
                    errorMessageContainer.innerHTML = result.message;
                    if(result.redirect_url != null){
                        window.location.href = result.redirect_url
                    }
                    break;
                case 'server_error':
                    message = "We're experiencing some technical issues. Please try again shortly.";
                    errorMessageContainer.innerHTML = message;
                    break;
                case 'unexpected_error':
                    message = "Something went wrong. Please refresh the page or try again later.";
                    errorMessageContainer.innerHTML = message;
                    break;
                default:
                    errorMessageContainer.innerHTML = response.message || "An unknown error occurred.";
            }            
            errorMessageContainer.classList.remove("hidden");
            console.log("Container", errorMessageContainer)
            return;
        } 
        
        if(result.status == 'success'){
            errorMessageContainer.classList.add("hidden");
            showToastNotification('success', result.message)
            if(result.next_url == null){
                window.location.reload();
            }else{
                window.location.href = result.next_url
            }
        }
        

    } catch(error){
        console.error("Error:", error);
        showToastNotification('error', error);
    } finally{
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}


// for direct password reset while user is in session
function handleResetPassword(event){
    event.preventDefault();
    form = event.target;

    old_password = form.querySelector('[name="old_password"]').value;
    new_password = form.querySelector('[name="new_password"]').value;
    new_password2 = form.querySelector('[name="new_password2"]').value;

    if(old_password == new_password){
        message = "Your new password must be different from the current password."
        console.log(message);
        showToastNotification('warning', message);
        return;
    }
    if(new_password != new_password2){
        message = 'The new passwords you entered do not match. Please try again.';
        console.log(message);
        showToastNotification('warning', message);
        return;
    }

    formData = new FormData(form)
    const submitBtn = form.querySelector('button[type="submit"]');
    originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = `<i class="fa fa-spinner fa-spin"></i> Resetting your password...`;
    submitBtn.disabled = true;

    fetch(form.action, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){showToastNotification('success', data.message);}
        else{showToastNotification('danger', data.message);}
    })
    .catch(error => {
        console.error("Reset Password failed", error);
        showToastNotification('danger', error);
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    })

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


/* FOR DYNAMICALLY CHANGING SIZE TO UNITS IF THE PROPERTY IS NOT A LAND */
const listing_type_field = document.querySelector('#id_listing_type')
const sizeLabel = document.querySelector('label[for="id_size"]');
if(listing_type_field && sizeLabel){

    listing_type_field.addEventListener('change', function(){
        console.log('hello')
        if(listing_type_field.value == 'land'){
            sizeLabel.textContent = "Size";
        }
        if(listing_type_field.value == 'buy' || listing_type_field.value == 'rent'){
            sizeLabel.textContent = "Units";
        }
    });

}
 /* END FOR DYNAMICALLY CHANGING SIZE TO UNITS IF THE PROPERTY IS NOT A LAND */

const fav_icons = document.querySelectorAll('.fav-icon')

if (fav_icons){
    fav_icons.forEach(fav_icon => {
        fav_icon.addEventListener('click', function(event){
            event.preventDefault();
            icon = fav_icon.querySelector('i');
            productId = fav_icon.getAttribute('data-listing-id')
            
            if (icon.classList.contains("text-white")) {
                icon.classList.remove("text-white");
                icon.classList.add("text-red-600");
            } else {
                icon.classList.remove("text-red-600");
                icon.classList.add("text-white");
            }

            fetch('/listing/toggle-favourite/', {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCsrfToken(),  // Make sure this function returns the correct CSRF token
                },
                body: `product_id=${encodeURIComponent(productId)}`
            })
            .then(response => response.json())
            .then(data => {
                console.log("Response data", data);
                if (data.is_favourite) {
                    icon.classList.remove("text-white");
                    icon.classList.add("text-red-600");
                } else {
                    icon.classList.remove("text-red-600");
                    icon.classList.add("text-white");
                }

                // if user is not logged in, it trigger Alpine to show the login modal
                if(data.error == "Anonymous user"){
                    setTimeout(() => {
                        Alpine.store('modal').openLoginModal = true;
                    }, 500)
                }
            })
            .catch(error => {
                console.error('Error', error)
            });

        });
    });
}

function showToastNotification(notification_type, message){
    notificationId = `toast-${notification_type}`;
    notificationBox = document.getElementById(notificationId);
    notificationBox.querySelector('.notification-message').innerText = message;
    
    notificationBox.style.display = "flex";
    notificationBox.classList.add("fade-in");

    // Auto-hide after duration
    setTimeout(() => {
        notificationBox.classList.remove("fade-in");
        notificationBox.classList.add("fade-out");

        // After fade out animation completes
        setTimeout(() => {
            notificationBox.style.display = "none";
            notificationBox.classList.remove("fade-out");
        }, 500);
    }, 6000);
}

function submitContactForm(e){
    e.preventDefault();
    let form = e.target;
    formData = new FormData(form)

    const submitBtn = form.querySelector('button[type="submit"]');
    originalText = submitBtn.innerHTML   
    submitBtn.innerHTML = `<i class="fa fa-spinner fa-spin"></i> Sending Message...`;
    submitBtn.disabled = true; //prevent double click 

    fetch(form.action, {
        method: 'POST',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            showToastNotification('success', data.message)
            form.reset();
        } else{
            displayFormError(data.errors, form);
            console.log(data.errors)
            showToastNotification('warning', "Invalid form details");
        }
    })
    .catch(error => {
        console.error("Error", error)
        showToastNotification('danger', 'Something went wrong')
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    })
}

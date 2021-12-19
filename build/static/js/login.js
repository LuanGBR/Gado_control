
window.onload = function(){
    const username = document.getElementById('username')
    const password = document.getElementById('password')
    
}
    
function LocalValidationU(){
    CheckInputsU();
}

function LocalValidationP(){
    CheckInputsP();
}

function CheckInputsU (){
    const usernamevalue = username.value.trim()
    
    if (usernamevalue == ''){
        setErrorFor(username)
        return false
    } else{
        setSuccessFor(username)
        return true
    }
}

function CheckInputsP (){
    const passwordvalue = password.value.trim()
    
    if (passwordvalue == ''){
        setErrorFor(password)
        return false
    } else{
        setSuccessFor(password)
        return true
    }
}

function setErrorFor(input){
    const formGroup = input.parentElement;

    formGroup.className = 'form-group error'
}

function setSuccessFor(input){
    const formGroup = input.parentElement;

    formGroup.className = 'form-group success'
}


function FormLocalValidation(){
    const loading = document.getElementById('loadingScreen')
    

    if ((CheckInputsP()) && (CheckInputsU())){
        console.log("Hi");
        loading.style.display = 'flex';
    }


}

function initializeDropdowns(recruitersData, consultantsData, submissionID, user) {

    var recruiterElement = document.getElementById('recruiter_' + submissionID);
    var consultantElement = document.getElementById('consultant_' + submissionID);
    var dateElement = document.getElementById('dos_' + submissionID);

    recruiterElement.innerHTML = '';
    consultantElement.innerHTML = '';

    recruiterElement_dropdown = document.createElement('select');
    consultantElement_dropdown = document.createElement('select');
    
    var currentDate = new Date();
    var year = currentDate.getFullYear();
    var month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    var day = currentDate.getDate().toString().padStart(2, '0');

    var formattedDate = year + '-' + month + '-' + day;
    console.log(formattedDate);
    dateElement.innerHTML = formattedDate;



    // Populate the recruiter dropdown
    recruitersData.forEach(recruiter => {
        var option = document.createElement('option');
        option.value = recruiter.R_UserName;
        option.text = recruiter.R_Name;
        recruiterElement_dropdown.appendChild(option);
    });

    //recruiterElement.innerHTML = recruiterElement_dropdown.outerHTML;
    recruiterElement.appendChild(recruiterElement_dropdown);
    console.log('In the edit function: ', recruiterElement)

    // Populate the consultant dropdown
    consultantsData.forEach(consultant => {
        var option = document.createElement('option');
        option.value = consultant.C_Id;
        option.text = consultant.C_Name;
        consultantElement_dropdown.appendChild(option);
    });
    //consultantElement.innerHTML = consultantElement_dropdown.outerHTML;
    consultantElement.appendChild(consultantElement_dropdown);
    console.log('In the edit function: ', consultantElement)
}


function editSubmission(submissionID, user) {
    console.log('Line 32');
    console.log(submissionID);
    var dosElement = document.getElementById('dos_' + submissionID);
    var recruiterElement = document.getElementById('recruiter_' + submissionID);
    var consultantElement = document.getElementById('consultant_' + submissionID);
    var jobTitleElement = document.getElementById('JobTitle_' + submissionID);
    var impPartnerElement = document.getElementById('Imp_Partner_' + submissionID);
    var endClientElement = document.getElementById('EndClient_' + submissionID);
    var endClientLocationElement = document.getElementById('EndClientLocation_' + submissionID);
    var partnerNameElement = document.getElementById('PartnerName_' + submissionID);
    var partnerContactElement = document.getElementById('PartnerContact_' + submissionID);

    // Enable editing for the elements
    dosElement.contentEditable = true;
    recruiterElement.disabled = false;
    consultantElement.disabled = false;
    jobTitleElement.contentEditable = true;
    impPartnerElement.contentEditable = true;
    endClientElement.contentEditable = true;
    endClientLocationElement.contentEditable = true;
    partnerNameElement.contentEditable = true;
    partnerContactElement.contentEditable = true;

    // Add a CSS class to indicate editing mode
    dosElement.classList.add('editable');
    recruiterElement.classList.add('editable');
    consultantElement.classList.add('editable');
    jobTitleElement.classList.add('editable');
    impPartnerElement.classList.add('editable');
    endClientElement.classList.add('editable');
    endClientLocationElement.classList.add('editable');
    partnerNameElement.classList.add('editable');
    partnerContactElement.classList.add('editable');

    initializeDropdowns(recruitersData, consultantsData, submissionID, user);

    // Change the edit button to save button
    var editButton = document.getElementById('editbutton_' + submissionID);
    editButton.innerHTML = 'Save';
    editButton.onclick = function () {
        saveSubmission(submissionID,user);
    };
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Function to handle the save button click
function saveSubmission(submissionId,user) {
    // Get the elements that were made editable
    var dosElement = document.getElementById('dos_' + submissionId);
    var recruiterElement = document.getElementById('recruiter_' + submissionId);
    var consultantElement = document.getElementById('consultant_' + submissionId);
    var jobTitleElement = document.getElementById('JobTitle_' + submissionId);
    var impPartnerElement = document.getElementById('Imp_Partner_' + submissionId);
    var endClientElement = document.getElementById('EndClient_' + submissionId);
    var endClientLocationElement = document.getElementById('EndClientLocation_' + submissionId);
    var partnerNameElement = document.getElementById('PartnerName_' + submissionId);
    var partnerContactElement = document.getElementById('PartnerContact_' + submissionId);
    // Disable editing for the elements
    
    dosElement.contentEditable = false;
    recruiterElement.disabled = true;
    consultantElement.disabled = true;
    jobTitleElement.contentEditable = false;
    impPartnerElement.contentEditable = false;
    endClientElement.contentEditable = false;
    endClientLocationElement.contentEditable = false;
    partnerNameElement.contentEditable = false;
    partnerContactElement.contentEditable = false;
    
    //Get the updates values from the editable elemnts
    var updatedSubmission = {
        S_DOS: dosElement.innerHTML,
        S_RecruiterId: recruiterElement.firstChild.value,
        S_ConsultantId: consultantElement.firstChild.value,
        S_ConsultantJobTitle: jobTitleElement.innerHTML,
        S_ImplementationPartner: impPartnerElement.innerHTML,
        S_EndClient: endClientElement.innerHTML,
        S_EndClientLocation: endClientLocationElement.innerHTML,
        S_ImplementationPartner_Name: partnerNameElement.innerHTML,
        S_ImplementationPartner_Contact: partnerContactElement.innerHTML
    };

    // Remove the CSS class indicating editing mode
    dosElement.classList.remove('editable');
    recruiterElement.classList.remove('editable');
    consultantElement.classList.remove('editable');
    jobTitleElement.classList.remove('editable');
    impPartnerElement.classList.remove('editable');
    endClientElement.classList.remove('editable');
    endClientLocationElement.classList.remove('editable');
    partnerNameElement.classList.remove('editable');
    partnerContactElement.classList.remove('editable');

    console.log(updatedSubmission);
    //Send the updated submission data to the server
    fetch(submissionId + '/' + 'highlight/', {
        method: 'PUT',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': "application/json"
        },
        body: JSON.stringify(updatedSubmission)
    }).then(response => response.json())
        .then(data => {
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch(error => {
            console.log(error);
        });


    // Change the save button back to edit button
    var editButton = document.getElementById('editbutton_' + submissionId);
    editButton.innerHTML = 'Edit';
    editButton.onclick = function () {
        editSubmission(submissionId,user);
    };
}

// Function to handle the delete button click
function deleteSubmission(submissionId) {
    // Perform the delete operation or any other necessary action
    console.log('Delete submission with ID:', submissionId);
    fetch(submissionId + '/' + 'highlight/', {
        method: 'DELETE',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': "application/json"
        }
    }).then(response => response.json())
        .then(data => {
            setTimeout(() => {
                console.log(window.location);
                window.location.reload();
            }, 1000);
        })
        .catch(error => {
            console.log(error);
        });

}

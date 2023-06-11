// the validation of the  password in the sign up page 
function CustomValidation(input) {
	this.invalidities = [];
	this.validityChecks = [];

	//add reference to the input node
	this.inputNode = input;

	//trigger method to attach the listener
	this.registerListener();
}

CustomValidation.prototype = {
	addInvalidity: function(message) {
		this.invalidities.push(message);
	},
	getInvalidities: function() {
		return this.invalidities.join('. \n');
	},
	checkValidity: function(input) {
		for ( var i = 0; i < this.validityChecks.length; i++ ) {

			var isInvalid = this.validityChecks[i].isInvalid(input);
			if (isInvalid) {
				this.addInvalidity(this.validityChecks[i].invalidityMessage);
			}

			var requirementElement = this.validityChecks[i].element;

			if (requirementElement) {
				if (isInvalid) {
					requirementElement.classList.add('invalid');
					requirementElement.classList.remove('valid');
				} else {
					requirementElement.classList.remove('invalid');
					requirementElement.classList.add('valid');
				}

			} // end if requirementElement
		} // end for
	},
	checkInput: function() { // checkInput now encapsulated

		this.inputNode.CustomValidation.invalidities = [];
		this.checkValidity(this.inputNode);

		if ( this.inputNode.CustomValidation.invalidities.length === 0 && this.inputNode.value !== '' ) {
			this.inputNode.setCustomValidity('');
		} else {
			var message = this.inputNode.CustomValidation.getInvalidities();
			this.inputNode.setCustomValidity(message);
		}
	},
	registerListener: function() { //register the listener here

		var CustomValidation = this;

		this.inputNode.addEventListener('keyup', function() {
			CustomValidation.checkInput();
		});


	}

};





var passwordValidityChecks = [
	{
		isInvalid: function(input) {
			return input.value.length < 8 | input.value.length > 100;
		},
		invalidityMessage: 'This input needs to be between 8 and 100 characters',
		element: document.querySelector('label[for="password"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function(input) {
			return !input.value.match(/[0-9]/g);
		},
		invalidityMessage: 'At least 1 number is required',
		element: document.querySelector('label[for="password"] .input-requirements li:nth-child(2)')
	},
	{
		isInvalid: function(input) {
			return !input.value.match(/[a-z]/g);
		},
		invalidityMessage: 'At least 1 lowercase letter is required',
		element: document.querySelector('label[for="password"] .input-requirements li:nth-child(3)')
	},
	{
		isInvalid: function(input) {
			return !input.value.match(/[A-Z]/g);
		},
		invalidityMessage: 'At least 1 uppercase letter is required',
		element: document.querySelector('label[for="password"] .input-requirements li:nth-child(4)')
	}
];

var passwordRepeatValidityChecks = [
	{
		isInvalid: function() {
			return passwordRepeatInput.value != passwordInput.value;
		},
		invalidityMessage: 'This password needs to match the first one'
	}
];





var passwordInput = document.getElementById('password');
var passwordRepeatInput = document.getElementById('password2');



passwordInput.CustomValidation = new CustomValidation(passwordInput);
passwordInput.CustomValidation.validityChecks = passwordValidityChecks;

passwordRepeatInput.CustomValidation = new CustomValidation(passwordRepeatInput);
passwordRepeatInput.CustomValidation.validityChecks = passwordRepeatValidityChecks;



var inputs = document.querySelectorAll('input:not([type="submit"])');


var submit = document.querySelector('input[type="submit"');
var form = document.getElementById('registration');

function validate() {
	for (var i = 0; i < inputs.length; i++) {
		inputs[i].CustomValidation.checkInput();
	}
}

submit.addEventListener('click', validate);
form.addEventListener('submit', validate);

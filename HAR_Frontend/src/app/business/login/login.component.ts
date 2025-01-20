import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';

import { RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UserLoginAuthInterface, UserRegisAuthInterface } from '../../shared/utils/types/user.interfaces';
import { AuthService } from '../../shared/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterLink, ReactiveFormsModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent implements AfterViewInit {

  form_signUp!: FormGroup;
  form_signIn!: FormGroup;

  constructor(
    private fb: FormBuilder, 
    private authService: AuthService
  ) 
  {
    this.initiateForms();
  }
  
  // Toggle between Log in & Sign up Sections
  @ViewChild('boxContainer') boxContainer!: ElementRef;
  @ViewChild('leftToggleButton') signinBtn!: ElementRef;
  @ViewChild('rightToggleButton') loginBtn!: ElementRef;

  ngAfterViewInit(): void {

    let toggleLogin = this.loginBtn.nativeElement;
    let toggleSignin = this.signinBtn.nativeElement;
    let container = this.boxContainer.nativeElement;

    toggleSignin.addEventListener('click', () => {
        container.classList.add('active');
    })

    toggleLogin.addEventListener('click', () => {
      container.classList.remove('active');
  })

  }

  // Forms
  initiateForms(): void {
    this.form_signIn = this.fb.nonNullable.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });

    this.form_signUp = this.fb.group({
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    username: ['', Validators.required],
    email: ['', Validators.required],
    password: ['', Validators.required]
    });
  }

  onSignIn(): void {
    if (this.form_signIn.valid) {
      console.log('Form Data', this.form_signIn.value)
      console.log(this.form_signIn.getRawValue() as UserLoginAuthInterface)

      this.authService.logUser(this.form_signIn.getRawValue() as UserLoginAuthInterface);
    }
  }

  onSignUp(): void {
    if (this.form_signUp.valid) {
      console.log('Form Data', this.form_signUp.value)
      console.log(this.form_signUp.getRawValue() as UserRegisAuthInterface)

      this.authService.registerNewUser(this.form_signUp.getRawValue() as UserRegisAuthInterface).subscribe(
        (response) => { console.log('response', response); }
      );
    }
  }

}

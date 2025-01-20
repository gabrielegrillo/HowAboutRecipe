import { Injectable, signal } from '@angular/core';
import { UserAuth, UserLoggedInfo, UserLoginAuthInterface, UserRegisAuthInterface, UserToken } from '../utils/types/user.interfaces';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private serverUrl: string = 'http://localhost:8000/api/users/';

  // Register mandi solo i dati, torna una risposta affermativa
  // Dopo attivi dalla mail, altrimenti neinte login
  // Dopo fai login e ti torna il codice da salvare

  private currentUserSignal = signal<UserLoggedInfo | undefined | null>(undefined);
  private currentUserSubject = new BehaviorSubject<UserLoggedInfo | undefined | null>(undefined);

  constructor(private httpClient: HttpClient, private router: Router) {}

  registerNewUser(user: UserRegisAuthInterface): Observable<any> {
    return this.httpClient.post(this.serverUrl + 'register/', user);
  }

  logUserIn(user: UserLoginAuthInterface): void {
    this.httpClient.post<UserToken>(this.serverUrl + 'login/', user).subscribe(
      (response) => {
        console.log('response', response);

        localStorage.setItem('token', response.access);
        this.currentUserSignal.set(response as UserLoggedInfo);
        this.currentUserSubject.next(response as UserLoggedInfo);

        this.router.navigateByUrl('/');
      });

  }

  logUserOut(): void {
    if (this.isUserLoggedIn()) {
      this.currentUserSignal.set(null);
      this.currentUserSubject.next(null);
      localStorage.setItem('token', '');
    }
  }

  checkIfLoggedInFirstTime() : Subject<UserLoggedInfo | undefined | null> {
    this.httpClient.get<UserLoggedInfo>(this.serverUrl + 'detail/')
    .subscribe({
      next: (response) => {
        this.currentUserSignal.set(response as UserLoggedInfo);
        this.currentUserSubject.next(response as UserLoggedInfo);
      },
      error: () => {
        this.currentUserSignal.set(null);
        this.currentUserSubject.next(null);
      }
    });

    return this.currentUserSubject;
      // (response) => {
      //   console.log('response', response);
      //   localStorage.setItem('token', response.access);
      //   this.currentUserSignal.set(user);
      //   this.router.navigateByUrl('/');
      // });
  }


  isUserUnknown(): boolean { return this.currentUserSignal() === undefined; }
  isUserLoggedOut(): boolean { return this.currentUserSignal() === null; }
  isUserLoggedIn(): boolean { return !this.isUserLoggedOut() && !this.isUserUnknown(); }

  getCurrentUser() { return this.currentUserSignal(); }
}

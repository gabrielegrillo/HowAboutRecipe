import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashService {
  private pathToDashboard: Subject<string> = new BehaviorSubject<string>("DashBoard");
  currentPathToDashboard$ = this.pathToDashboard.asObservable()

  constructor() { }

  sendCurrentPath(path: string): void {
    this.pathToDashboard.next(path);
  }

  getCurrentPath(): Observable<string> {
    return this.currentPathToDashboard$;
  }

}

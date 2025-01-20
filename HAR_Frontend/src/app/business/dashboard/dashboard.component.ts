import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { AuthService } from '../../shared/services/auth.service';
import { DashService } from '../../shared/services/dash.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  currentPathToContent: string[] = ["Dashboard"];

  constructor(
    private authService: AuthService, 
    private dashService: DashService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.dashService.getCurrentPath().subscribe(
      (path) => {
        setTimeout(() => {
          this.currentPathToContent = path.split('.')
                                          .map(word => word.charAt(0).toUpperCase() + word.slice(1));
        });
      });
  }

  doLogOut(): void {
    this.authService.logUserOut();
    this.router.navigateByUrl('/');
  }

  getUserName(): string {
    if (!this.authService.isUserLoggedIn()) return "Miao"

    let first_name = this.authService.getCurrentUser()?.first_name;
    let last_name = this.authService.getCurrentUser()?.last_name;
    return first_name ?? '' + last_name ?? '';
  }

}

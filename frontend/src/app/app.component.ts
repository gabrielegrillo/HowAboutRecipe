import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

/* Temp Import to Test */
import { HeaderComponent } from './shared/components/header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'howaboutrecipe';
}

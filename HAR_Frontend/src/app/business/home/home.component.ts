import { Component } from '@angular/core';

import { FooterComponent } from '../../shared/components/footer/footer.component';
import { HeaderComponent } from '../../shared/components/header/header.component';
import { HeroShowcaseComponent } from '../../shared/components/hero-showcase/hero-showcase.component';
import { CategoryShowcaseComponent } from '../../shared/components/category-showcase/category-showcase.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    FooterComponent,
    HeaderComponent,
    HeroShowcaseComponent,
    CategoryShowcaseComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}

import { Component } from '@angular/core';
import { HeaderComponent } from '../../shared/components/header/header.component';
import { FooterComponent } from '../../shared/components/footer/footer.component';
import { CategoryShowcaseComponent } from '../../shared/components/category-showcase/category-showcase.component';

@Component({
  selector: 'app-not-found-page',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, CategoryShowcaseComponent],
  templateUrl: './not-found-page.component.html',
  styleUrl: './not-found-page.component.css'
})
export class NotFoundPageComponent {

}

import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DashService } from '../../services/dash.service';
import { RecipeService } from '../../services/recipe.service';
import { AuthService } from '../../services/auth.service';
import { RecipeInterface } from '../../utils/types/recipe.interfaces';

@Component({
  selector: 'app-dash-basic',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './dash-basic.component.html',
  styleUrl: './dash-basic.component.css'
})
export class DashBasicComponent implements OnInit {
  
  userRecipes: RecipeInterface[] = [];

  constructor(
    private dashService: DashService, 
    private recipeService: RecipeService,
    private authService: AuthService
  ) {}
  
  ngOnInit(): void {
    let currentUser = this.authService.getCurrentUser();
    if (!currentUser) return;

    this.recipeService.getRecipesOfUser(currentUser.username).subscribe(
      (response) => {
        console.log('response', response);
        this.userRecipes = response;
      }
    )

    this.dashService.sendCurrentPath("Dashboard.Home");
  }

  getImagePath(title: string): string {
    return `/recipes-images/${this.recipeService.convertTitleToImageName(title)}`;
  }
  
}

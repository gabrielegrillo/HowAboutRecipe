import { Component, OnInit } from '@angular/core';
import { DashService } from '../../services/dash.service';
import { AuthService } from '../../services/auth.service';
import { RecipeService } from '../../services/recipe.service';
import { RecipeInterface } from '../../utils/types/recipe.interfaces';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dash-recipes',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './dash-recipes.component.html',
  styleUrl: './dash-recipes.component.css'
})
export class DashRecipesComponent implements OnInit {

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

    this.dashService.sendCurrentPath("Dashboard.Recipes");
  }

  getImagePath(title: string): string {
    return `/recipes-images/${this.recipeService.convertTitleToImageName(title)}`;
  }
  
  doDelete(recipe_id: string): void {

  }

  makePrivate(recipe_id: string): void {
    
  }

}

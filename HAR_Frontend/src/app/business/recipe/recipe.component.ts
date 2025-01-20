import { Component, input, OnInit } from '@angular/core';
import { HeaderComponent } from '../../shared/components/header/header.component';
import { FooterComponent } from "../../shared/components/footer/footer.component";
import { RecipeService } from '../../shared/services/recipe.service';
import { RecipeInterface } from '../../shared/utils/types/recipe.interfaces';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-recipe',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, RouterLink],
  templateUrl: './recipe.component.html',
  styleUrl: './recipe.component.css'
})
export class RecipeComponent implements OnInit {
  recipeId = input.required<string>();
  recipeShown: RecipeInterface = {} as RecipeInterface;

  constructor(private recipeService: RecipeService) {}
  
  ngOnInit(): void {
    this.recipeService.getRecipeById(this.recipeId()).subscribe((recipes: RecipeInterface) => {
        console.log('recipe', this.recipeId(), recipes);
        this.recipeShown = recipes;
      })
  }

  getRecipeDifficultyAsString(difficulty: number): string {
    return this.recipeService.convertRecipeDifficultyToString(difficulty);
  }

  getPreparationTimeAsString(minutes: number): string {
    return this.recipeService.convertPrepationTimeToString(minutes);
  }

  getImagePath(title: string): string {
    return `/recipes-images/${this.recipeService.convertTitleToImageName(title)}`;
  }

  getStepsAsArray(steps: string): string[] {
    return steps.split(/\s*\d+\.\s*/).filter(step => step.trim() !== "");
  }
}

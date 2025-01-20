import { Component, Input, OnInit } from '@angular/core';
import { RecipeInterface } from '../../utils/types/recipe.interfaces';
import { RecipeService } from '../../services/recipe.service';
import { RouterLink } from '@angular/router';
import { min } from 'rxjs';

@Component({
  selector: 'app-category-showcase',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './category-showcase.component.html',
  styleUrl: './category-showcase.component.css'
})
export class CategoryShowcaseComponent implements OnInit {
  @Input() cardStyle: string = "card-blue";
  @Input() categoryTitle: string = "Titolo della categoria";
  @Input() tagToSearch: string = "__generics";

  recipesToShow: RecipeInterface[] = [];

  constructor(private recipeService: RecipeService) {}

  ngOnInit(): void {
    if(this.tagToSearch === "__generics"){ 
      this.recipeService.getRecipesGenerics().subscribe((recipes: RecipeInterface[]) => {
        console.log('recipe', recipes);
        this.recipesToShow = recipes;
      });
    
      return;
    }

    this.recipeService.getRecipesByTag(this.tagToSearch).subscribe((recipes: RecipeInterface[]) => {
        console.log('recipe', recipes);
        this.recipesToShow = recipes;
    });
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
}

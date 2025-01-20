import { Component, ViewChild, ElementRef, AfterViewInit, OnInit } from '@angular/core';
import { RecipeInterface } from '../../utils/types/recipe.interfaces';
import { RecipeService } from '../../services/recipe.service';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-hero-showcase',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './hero-showcase.component.html',
  styleUrl: './hero-showcase.component.css'
})
export class HeroShowcaseComponent implements OnInit, AfterViewInit{

  public recipesData: RecipeInterface[] = [] 

  @ViewChild('showcaseCarousel') showcaseCarousel!: ElementRef;
  @ViewChild('nextButton') nextButton!: ElementRef;
  @ViewChild('prevButton') prevButton!: ElementRef;

  constructor(private recipeService: RecipeService) {}

  ngOnInit(): void {
    this.recipeService.getRecipesGenerics().subscribe((recipes: RecipeInterface[]) => {
      console.log('recipe', recipes);
      this.recipesData = recipes.reverse().slice(0, 5);
    });
  }

  ngAfterViewInit(): void {
    let carousel = this.showcaseCarousel.nativeElement;

    this.nextButton.nativeElement.addEventListener('click', () => {
      console.log("Next Pressed");
  
      carousel.appendChild(carousel.children[0]);    
    });
    
    this.prevButton.nativeElement.addEventListener('click', () => {
      console.log("Prev Pressed");
      
      carousel.prepend(carousel.children[carousel.children.length - 1]);
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

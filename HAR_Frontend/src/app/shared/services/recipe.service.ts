import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RecipeInterface } from '../utils/types/recipe.interfaces';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RecipeService {
  private serverUrl: string = "http://localhost:8000/api/recipes/"

  constructor(private httpClient: HttpClient) { 
  }

  getRecipeById(id: string): Observable<RecipeInterface> {
      return this.httpClient.get<RecipeInterface>(this.serverUrl + `${id}/`,)
  }

  getRecipesByTag(tag: string): Observable<RecipeInterface[]> {
    return this.httpClient.get<RecipeInterface[]>(this.serverUrl + `tag/${tag}/`);
  }

  getRecipesGenerics():
  Observable<RecipeInterface[]> {
    return this.httpClient.get<RecipeInterface[]>(this.serverUrl + 'home/');
  }

  // Utils 
  convertPrepationTimeToString(minutes: number): string {
    return minutes + " min";
  }

  convertRecipeDifficultyToString(difficulty: number): string {
    if(difficulty === 1 || difficulty === 2) return "Easy";
    if(difficulty === 4 || difficulty === 5) return "Hard";

    return "Medium";
  }

  convertTitleToImageName(title: string): string {
    return title.toLowerCase().replace(/\s+/g, '-') + '.jpg';
  }

  
}

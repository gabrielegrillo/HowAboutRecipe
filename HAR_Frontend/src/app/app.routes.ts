import { Routes } from '@angular/router';

import { LoginComponent } from './business/login/login.component';
import { RecipeComponent } from './business/recipe/recipe.component';
import { HomeComponent } from './business/home/home.component';

export const routes: Routes = [
  { 
    path: '', 
    redirectTo: 'home',
    pathMatch: 'full' 
  },
  { 
    path: 'home', 
    loadComponent: () => import('./business/home/home.component').then((c) => c.HomeComponent )
  },
  { 
    path: 'login', 
    component: LoginComponent 
  },
  {
    path: 'recipes/:recipeId',
    loadComponent: () => import('./business/recipe/recipe.component').then((c) => c.RecipeComponent),
  },

  /* Lazy Loading -> loadComponent: () => import('./business/home/home.component').then((c) => c.HomeComponent ) */
  /* ---- Not Found Page ---- */
  // {
  //   path: '**',
  //   redirectTo: 'home',
  //   pathMatch: 'full'
  // }
];

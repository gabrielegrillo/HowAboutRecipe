import { inject } from "@angular/core"
import { AuthService } from "../services/auth.service"
import { Router } from "@angular/router";
import { map, Observable } from "rxjs";


export const authGuard: () => Observable<boolean> = () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    return authService.checkIfLoggedInFirstTime().pipe(
        map((currentUser) => {
            if (!currentUser) {
                router.navigateByUrl('/');
                console.log("Non Autorizzato");
                return false;
            }

            return true;
        })
    );
}
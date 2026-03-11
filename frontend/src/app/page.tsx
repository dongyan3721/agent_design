import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { DEFAULT_LOCALE, ROUTES, withLocale } from "@/lib/constants";

export default async function RootPage() {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (accessToken) {
    redirect(withLocale(ROUTES.DASHBOARD, DEFAULT_LOCALE));
  }

  redirect(withLocale(ROUTES.LOGIN, DEFAULT_LOCALE));
}

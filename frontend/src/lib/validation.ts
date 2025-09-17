import { z } from "zod";

export const idSchema = z.object({
  id: z
    .string()
    .trim()
    .min(3, "ID חייב להיות לפחות 3 תווים")
    .max(64, "ID ארוך מדי (מקסימום 64)")
    .regex(/^[A-Za-z0-9_-]+$/, "מותר רק אותיות/ספרות/_/-"),
});

export type IdInput = z.infer<typeof idSchema>;

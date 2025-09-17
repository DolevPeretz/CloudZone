import React, { useState } from "react";
import { Card } from "../../components/ui/Card";
import { LabeledInput } from "../../components/ui/Input";
import { Button } from "../../components/ui/Button";
import { Status } from "../../components/ui/Status";
import type { ApiClient } from "../../lib/types";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { idSchema, type IdInput } from "../../lib/validation";
import toast from "react-hot-toast";

export const DeleteIdForm: React.FC<{ api: ApiClient }> = ({ api }) => {
  const [status, setStatus] = useState<{
    kind: "info" | "success" | "error";
    text: string;
  } | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<IdInput>({
    resolver: zodResolver(idSchema),
  });

  const onSubmit = async ({ id }: IdInput) => {
    setStatus(null);
    try {
      const data = await api.deleteId(id.trim());
      toast.success("נמחק (אם היה קיים)");
      setStatus({
        kind: "success",
        text: `נמחק (אם היה קיים): ${JSON.stringify(data)}`,
      });
      reset();
    } catch (err: any) {
      const msg = String(err?.message || err);
      toast.error(msg);
      setStatus({ kind: "error", text: msg });
    }
  };

  return (
    <Card title="מחיקת מזהה (DELETE)">
      <form className="space-y-3" onSubmit={handleSubmit(onSubmit)}>
        <LabeledInput
          label="Customer ID"
          placeholder="למשל: 1234-AB"
          disabled={isSubmitting}
          {...register("id")}
        />
        {errors.id && (
          <div className="text-sm text-red-600">{errors.id.message}</div>
        )}
        <div className="flex gap-2">
          <Button type="submit" loading={isSubmitting}>
            מחק
          </Button>
        </div>
      </form>
      <Status kind={status?.kind} text={status?.text} />
    </Card>
  );
};
